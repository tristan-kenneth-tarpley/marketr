from google.oauth2 import service_account
import pandas
import pandas_gbq
import pyarrow

class BigQuery(object):
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": "marketr-app",
            "private_key_id": "9fe4fdebc713ddb1fbba51eb26d40c7e59b0900e",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC8lUWYNFOvdEVr\n0ibh6qpXAiHA/iFEzR4LnRVtGdHat6q7YDkSBR6rdS3Dei1JzKBeuwwWjiFWtIAO\nJ4Ect14s8P+hY6rc0/NlkKqN+p+Z6v4+O2wgEnNEkQ5WLaq38BRK2iBX+nsmKyBE\nKpqno4fDYEYs6TQCrJA7S57jVDeqKtJvbf2C6hobmN4LVym5iHdx7k4ymneLjb7w\nKpnsP3VHNMttNkiUBOlE7SfrwthFz4ihJ2ym1BU5q9MwVyyMtgFY0mjqTBPZhv6e\nFtFRVPc+Y+rG7mR8MRirNViPYyUiO69UfZo7z4acnPDCBwUe30vmlFYUy2oJCx8h\nXTxeJzKzAgMBAAECggEANW2XJ42frgRjjK4f/P6WnwsIFB0LwOnaGtE42k2n4m8J\nzIdw89WGgG409n5daVyzjNMylAtVj7KY2ym/Dys2X8YxroBFzsWv3jUT1SDN6fYl\nbO0574Y6qRDtvmW2yeEXZrOQ2UwqasBqJlXpthgDJUvX5e52IVHRlTMSA3b/RFLb\n+xo2Te16nkrcIeJzYtHmMKoF3qOEniUzFpenPMZ0V+/kAOvaVmMhX0d1KX1+wmOk\nR0HYNhBfCG7/+L1Q+CJckqxltIDQ7x3uP4TnbNZeHVSGwpOr3u2CksDKkZakrljm\nFHtjNT7Uc9WpfVkQg9IcchfDSgCk0NTWqSmwwb2U9QKBgQDhqkgpJPkxB7IJefkD\ntdToZAn9ih4NyLumSFizNXcsH2c7rvD5TqXpTnwNEH6fGpitwFb89AjZGhLnvxBW\nRm7pjOMMZgcI/gjAR0kzZ3gi8duY/9Z8Zxao+38cUnvee6qwxam+g4jXGW2I9VO6\nMLtbqpZ6IFHJwgnmsd9zkWVKpQKBgQDV7uaRFrl74/n9OVHHADdTe/8Dn/6SHywO\nhkrOcuykUDC45QzW2Oz687+qxYAujdL2RoCgrEj4CxS/MCd7NWPreeLEpfyfz9n3\niK1wAS4gzaFO378WiADYut4qnLlN/FnvUwgP6SN7uWVrqPSXo4VBCIpj5z1wag60\na3z1TpOAdwKBgHSR/+CxJsB7Fy7qAQY3oZnCQ57jAA9ix/xnltpMHhl+x1b/UZ+X\nTwEr98zP3njVxlTK7KSScxei7m0kN445qAWhL5AyDCRLBb49lMSnCFoU0blBP0zX\n+86iy9CXk0EkZNIX6U1uqPtkOT7sa6ncjowVnNHNbDJqt66h56nNS6O5AoGARFTz\ndmJgyo6t+dEGKt8JzPOtJ7ZB9OBaDSWd3UVeCrnGZjhbGoDdaObUULKW18fbG2i3\nixqckAXSEaNK6RLLoJok8ZTnFRCp2WPhqgXmevnTTUMwYPz98Dv33HqEwcEZ5NSL\nnbFk8Q7tsy6bOZg0ZupYccKZoD9wBPbUSfJYMM8CgYEAxfqBKYUuuyztsI9Fi4fm\nHCvbqMFzVZEoSkVaX6zLXeJvCGz2nu8GDsOzNwc2RUU8ZQH3AV3Q96UqTLROp0QN\npEbA6CJWcEIT+Uyqz/boAobpc9QonOJN3fIS6hoAQPW9+/H1pIv8D7ndhA7J75ei\nN9f2PusTdbodD53SHcyteYg=\n-----END PRIVATE KEY-----\n",
            "client_email": "marketr@marketr-app.iam.gserviceaccount.com",
            "client_id": "103363973211179125545",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/marketr%40marketr-app.iam.gserviceaccount.com"
        }

        )
        self.project_id = 'marketr-app'
        
    def get(self, sql):
        try:
            return pandas_gbq.read_gbq(sql, project_id=self.project_id, credentials=self.credentials)
        except Exception as e:
            print(e)
            return None



class GoogleORM(BigQuery):
    def __init__(self, company_name):
        super().__init__()
        disallow = ["(", ")", ";", ",", "."]
        for d in disallow:
            company_name = company_name.replace(d, "")

        self.company_name = company_name.replace(" ", "_").lower()

    def google_performance(self):
        sql = f"""
        SELECT ctr, clicks, conversions, cost, impressions, interactions, week FROM `{self.project_id}.{self.company_name}_google.ACCOUNT_PERFORMANCE_REPORT` order by week desc
        """
        return self.get(sql)
    
    def fb_performance(self):
        sql = f"""
        SELECT impressions, ctr, clicks, reach, cpc, cpm, spend, frequency, date_start as week FROM `{self.project_id}.{self.company_name}_facebook.ads_insights` 
        """
        return self.get(sql)

    def agg(self):
        google = f"""
        SELECT ctr, clicks, cost/1000000 as cost, conversions, impressions, interactions, week, null as date_stop

        FROM `{self.project_id}.{self.company_name}_google.ACCOUNT_PERFORMANCE_REPORT`"""

        facebook = f"""SELECT ctr, clicks, spend as cost, null as conversions, impressions, reach as interactions, CAST(EXTRACT(DATE FROM date_start) AS string) as week, CAST(EXTRACT(DATE FROM date_stop) AS string) as date_stop
        FROM `{self.project_id}.{self.company_name}_facebook.ads_insights`"""

        g_fb = google + " union all " + facebook
        # return self.get(g_fb)
        try:
            return self.get(g_fb)
        except:
            try:
                return self.get(google)
            except:
                try:
                    return self.get(facebook)
                except:
                    return None

    def social_campaigns(self):
        query = f"""
        select distinct 'facebook' as type, effective_status as state, name as campaign_name, id as campaign_id from `{self.project_id}`.`{self.company_name}_facebook`.`campaigns`
        """

        return self.get(query)
    
    def search_campaigns(self):
        query = f"""
        select distinct 'google' as type, campaignstate as state, campaign as campaign_name, campaignid as campaign_id from `{self.project_id}`.`{self.company_name}_google`.`AD_PERFORMANCE_REPORT`
        """

        return self.get(query)

    def cost_past_7(self):
        query = f"""
        select sum(cost) as cost from (
            select sum(spend / 1000) as cost from `{self.project_id}`.`{self.company_name}_facebook`.`ads_insights` as ai

            WHERE EXTRACT(DATE FROM date_start) > DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)

            union all

            select sum(cost / 1000000) as cost from `{self.project_id}`.`{self.company_name}_google`.`ACCOUNT_PERFORMANCE_REPORT` as acc

            WHERE EXTRACT(DATE FROM day) > DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        )
        """

        return self.get(query)

    def social_index(self, _range):

        facebook = f"""
            select distinct
                (select sum(distinct spend) from `{self.project_id}`.`{self.company_name}_facebook`.`ads_insights` where date_diff(CURRENT_DATE(), CAST(DATE(date_start) AS DATE), day) <= {_range}) as _cost,

                (select _1d_click + _7d_click + _28d_click from unnest(ai.actions) where action_type = 'omni_purchase') as conversions,

                ads.creative.id, ads.adset_id, ads.campaign_id,

                creative.image_url as thumbnail_url, creative.body,

                ai.ad_name as ad_name, ai.date_start as date_start, ai.ctr, ai.cpc, ai.impressions, ai.clicks, ai.spend as cost, 

                ca.name as campaign_name,
                null as daily_budget

            from `{self.project_id}`.`{self.company_name}_facebook`.`ads_insights` as ai

            join `{self.project_id}`.`{self.company_name}_facebook`.`ads` as ads
            on ai.ad_id = ads.id

            join `{self.project_id}`.`{self.company_name}_facebook`.`adcreative` as creative
            on creative.id = ads.creative.id

            join `{self.project_id}`.`{self.company_name}_facebook`.`campaigns` as ca
            on ca.id = ads.campaign_id


            where campaign_name is not null
            and date_diff(CURRENT_DATE(), CAST(DATE(ai.date_start) AS DATE), day) <= {_range}
            and creative.image_url is not null

            order by date_start

        """
        
        return self.get(facebook)
    
    def search_index(self, _range):
        retry_count = 0

        google = f"""
            select 

            distinct 

            rep.imageadurl, rep.campaign as campaign_name, rep.day as date_start, rep.campaignid, rep.adgroupid, rep.adid, rep.keywordid, rep.finalurl, rep.headline1, rep.headline2, rep.description, rep.ctr, rep.clicks, rep.conversions, rep.cost / 1000000 as cost, rep.impressions, campaign.budget / 1000000 as daily_budget,

            (
            select sum(cost) from (
                select distinct cost / 1000000 as cost from `{self.project_id}`.`{self.company_name}_google`.`ACCOUNT_PERFORMANCE_REPORT`
                where date_diff(CURRENT_DATE(), CAST(DATE(day) AS DATE), day) <= {_range}
            )) as _cost


            from `{self.project_id}`.`{self.company_name}_google`.`AD_PERFORMANCE_REPORT` as rep

            join `{self.project_id}`.`{self.company_name}_google`.`CAMPAIGN_PERFORMANCE_REPORT` as campaign
            on campaign.campaignid = rep.campaignid

            where rep.campaign is not null and date_diff(CURRENT_DATE(), CAST(DATE(rep.day) AS DATE), day) <= {_range} and rep.campaignstate <> 'paused' 
        """

        second_google = f"""

            select 

            distinct 

            null as imageadurl, rep.campaign as campaign_name, rep.day as date_start, rep.campaignid, rep.adgroupid, rep.adid, rep.keywordid, rep.finalurl, rep.headline1, rep.headline2, rep.description, rep.ctr, rep.clicks, rep.conversions, rep.cost / 1000000 as cost, rep.impressions, campaign.budget / 1000000 as daily_budget,

            (
            select sum(cost) from (
                select distinct cost / 1000000 as cost from `{self.project_id}`.`{self.company_name}_google`.`ACCOUNT_PERFORMANCE_REPORT`
                where date_diff(CURRENT_DATE(), CAST(DATE(day) AS DATE), day) <= {_range}
            )) as _cost


            from `{self.project_id}`.`{self.company_name}_google`.`AD_PERFORMANCE_REPORT` as rep

            join `{self.project_id}`.`{self.company_name}_google`.`CAMPAIGN_PERFORMANCE_REPORT` as campaign
            on campaign.campaignid = rep.campaignid

            where rep.campaign is not null and date_diff(CURRENT_DATE(), CAST(DATE(rep.day) AS DATE), day) <= {_range} and rep.campaignstate <> 'paused' 

        """

        retry_count = 1
        returned = self.get(google)

        if returned is not None:
            return returned
        else:
            returned = self.get(second_google)
            retry_count += 1
            if returned is not None:
                return returned
            else:
                return None

                



            
        