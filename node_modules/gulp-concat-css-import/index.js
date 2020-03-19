let gutil = require ('gulp-util')
let through = require ('through2')
let Buffer = require ('buffer').Buffer
let fs = require ('fs')
let url = require ('url')
let path = require ('path')
let flkit = require ('flkit')

let rootPath

const RegImport = /@import\s+url\s*\(\s*(?:[\'\"]?)([\w\/_\.\:\-]+\.css)(?:\?[^\'\"\)]*)?(?:[\'\"]?)\s*\)\s*[;]?/;
const ResourceRegExp = {
    background: /url\s*\(\s*([\'\"]?)([\w\-\/\.\@]+\.(?:png|jpg|gif|jpeg|ico|cur|webp))(?:\?[^\?\'\"\)\s]*)?\1\s*\)/ig,
    font: /url\s*\(\s*([\'\"]?)([^\'\"\?]+\.(?:eot|woff2|woff|ttf|svg|otf))([^\s\)\'\"]*)\1\s*\)/ig,
    filter: /src\s*=\s*([\'\"])?([^\'\"]+\.(?:png|jpg|gif|jpeg|ico|cur|webp))(?:\?[^\?\'\"\)\s]*)?\1\s*/ig
}
const RegInCss = [
    ResourceRegExp.background,
    ResourceRegExp.font,
    ResourceRegExp.filter
]

function isObject(obj) {
    return Object.prototype.toString.call(obj) === '[object Object]'
}
function isRemoteUrl(url) {
    if (!url) {
        return false
    }
    url = url.toLowerCase()
    return url.indexOf('http://') === 0 || url.indexOf('https://') === 0 || url.indexOf('//') === 0
}
function extend (target, ...sources) {
    let src, copy
    if (!target) {
        target = Array.isArray (sources[ 0 ]) ? [] : {}
    }
    sources.forEach (source => {
        if (!source) {
            return
        }
        for (let key in source) {
            src = target[ key ]
            copy = source[ key ]
            if (src && src === copy) {
                continue
            }
            if (isObject (copy)) {
                target[ key ] = extend (src && isObject (src) ? src : {}, copy)
            } else if (Array.isArray (copy)) {
                target[ key ] = extend ([], copy)
            } else {
                target[ key ] = copy
            }
        }
    })
    return target
}
function extractContentByFile(cssFile){
    let fileContent = ''

    if (fs.existsSync (cssFile)) {

        fileContent = fs.readFileSync (cssFile).toString ()
    }

    return fileContent
}
function extractCssTokenizeContent(baseCssFile, currentCssFile, fileContent){
    let tokens = (new flkit.CssTokenize (fileContent, { parseSelector : true })).run()
    let newTokens = []

    for(let token of tokens) {
        if(token.type === flkit.TokenType.CSS_IMPORT) {
            let match = RegImport.exec(token.value)

            if(!match) {
                throw new Error(`Can not parse @import in \`${token.value}\``, token.loc.start.line, token.loc.start.column)
                newTokens.push(token)
                continue
            }

            let importCssPath = match[1]

            if(isRemoteUrl(importCssPath)) {
                newTokens.push(token)
                continue
            }

            let importCssFile = getResolvePath(currentCssFile, importCssPath)
            if(importCssFile) {

                let importFileContent = extractContentByFile(importCssFile)
                let importFileTokens  = extractCssTokenizeContent(baseCssFile, importCssFile, importFileContent)

                importFileTokens = resolvePath(baseCssFile, importCssFile, importFileTokens)

                if (rootPath){
                    for (let i=0; i<importFileTokens.length; i++) {
                        if (importFileTokens[i].type === flkit.TokenType.CSS_SELECTOR){
                            importFileTokens[i].commentBefore.unshift({
                                value : `\n/**import from \`${importCssFile.replace(rootPath, '').replace(/\\/g, '/')}\` **/\n`
                            })
                            break
                        }
                    }
                }

                ;[].push.apply(newTokens, importFileTokens)
            }
        } else {
            newTokens.push(token)
        }
    }
    return newTokens
}
function resolvePath(baseCssFile, cssFile, tokens) {
    let newTokens = []

    tokens.forEach(token => {
        if(token.type === flkit.TokenType.CSS_VALUE) {
            RegInCss.some(item => {
                let flag = false

                token.ext.value.replace(item, (...args) => {
                    let resPath = args[2]

                    // only resolve relative path
                    if(resPath && !isRemoteUrl(resPath) && /^\.{2}\//.test(resPath)) {
                        flag = true

                        let baseLevel = baseCssFile.split(path.sep).length
                        let cssLevel  = cssFile.split(path.sep).length

                        let resolvedResPath;
                        let levelDiff = baseLevel - cssLevel

                        if(levelDiff === 0) {
                            return flag
                        }
                        else if(levelDiff > 0) {
                            resolvedResPath = url.resolve('../'.repeat(levelDiff), resPath)
                        }
                        else if(levelDiff < 0) {
                            resolvedResPath = url.resolve('x/'.repeat(-levelDiff), resPath)
                        }

                        token = extend({}, token)
                        token.value = token.value.replace(resPath, resolvedResPath)
                        token.ext.value = token.value
                    }

                    return flag
                })
            })
        }

        newTokens.push(token)
    })

    return newTokens
}
function getResolvePath(currentFile, filePath){
    if(path.isAbsolute(filePath)){
        return filePath
    }
    filePath = path.normalize (decodeURIComponent (url.parse (filePath).pathname))

    let currentFilePath = path.dirname(currentFile)

    let resolveFilePath = filePath
    if(filePath.indexOf(currentFilePath) !== 0)  {
        resolveFilePath = path.resolve(currentFilePath, filePath)
    }
    let currentPath = process.cwd() + path.sep
    if(resolveFilePath.indexOf(currentPath) === 0){
        resolveFilePath = resolveFilePath.slice(currentPath.length)
    }
    return resolveFilePath
}
function topCharset (tokens) {
    let charsetToken = null
    let newTokens = []

    tokens.forEach ((token, index) => {
        if (token.type === flkit.TokenType.CSS_CHARSET) {
            charsetToken = token
        } else {
            newTokens.push (token)
        }
    })

    if (charsetToken) {
        newTokens.unshift (charsetToken)
    }

    return newTokens
}
function breakAtRightBrace (tokens) {
    tokens.forEach (function (token) {
        if (token.type === flkit.TokenType.CSS_RIGHT_BRACE) {
            token.value = token.value + "\n"
        }
    })
}

module.exports = function (options) {

    rootPath = options.rootPath || ''
    let isCompress = options.isCompress || false

    return through.obj (function (file, enc, cb) {
        if (file.isNull ()) {
            this.push (file)
            return cb ()
        }

        if (file.isStream ()) {
            this.emit ('error', new gutil.PluginError ('gulp-concat-css-import', 'Streaming not supported'))
            return cb ()
        }

        let fileContent = String (file.contents.toString ())

        let tokens = extractCssTokenizeContent(file.path, file.path, fileContent)
        tokens = topCharset(tokens)

        if (isCompress){
            file.contents = new Buffer ((new flkit.CssCompress(tokens)).run())
        } else {
            breakAtRightBrace(tokens)
            file.contents = new Buffer (flkit.cssToken2Text(tokens))
        }

        this.push (file)
        cb ()
    })
}