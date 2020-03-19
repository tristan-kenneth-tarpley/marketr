## gulp-concat-css-import

## Quick Start

### 1.Installation

```bash
$ npm install --save gulp-concat-css-import
```

### 2.Usage
My css file is `combo.css`, '/resource/css/combo/src/combo.css' is relative path at website's root.
```css
@import url(../../page/hehe1.css);
@import url(../../page/hehe2.css);
```
hehe1.css
```css
.hehe1{
    color: #444;
}
```
hehe2.css
```css
@import url(hehe3.css);
.hehe2{
    background-color: #f00;
}
```
hehe3.css
```css
.hehe3{
    color: #000;
}
```
Finally, concated file is '/resource/css/combo/dest/combo.css', it's content as the following:
```css

/**import from `/resource/css/page/hehe1.css` **/
.hehe1{color:#444;}

/**import from `/resource/css/page/hehe2.css` **/

/**import from `/resource/css/page/hehe3.css` **/
.hehe3{color:#000;}
.hehe2{background-color:#f00;}
```

In my gulp file written like this:
```js
let concatImport = require('gulp-concat-css-import')

let rootPath = '/website/root/absolute/path'
let cssSrc = '/the/path/is/resource/css/combo/src'
let cssDest = '/the/path/is/resource/css/combo/dest'

gulp.task ('css', function () {
    gulp.src (cssSrc+'/**/*.css')
        .pipe (concatImport ({
            rootPath : rootPath,
            isCompress : false
        }))
        .pipe (gulp.dest (cssDest))
})
```