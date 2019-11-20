
# # coding: utf-8

# # In[29]:


# from google.oauth2 import service_account
# import pandas_gbq


# # In[30]:


# class BigQuery(object):
#     def __init__(self):
#         self.credentials = service_account.Credentials.from_service_account_info(
#             {
#             "type": "service_account",
#             "project_id": "marketr-app",
#             "private_key_id": "2b7740004c3a58d4f89d3f66e48514c286d2c797",
#             "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDi9cwp/CgmTq3d\n4WrWAjQHzQj2zm8R4onTGVpKdCeeCauFSGumSIIaKBgjnhCLz3MVZndPRUkqkhNZ\nysI5mXNay4vsEE9UrOfwcDcbMrDK+f2uTMwp5mSakJH0mt+g7/E9j8PA5x2xuqiw\ngOCs3PfqntjaOypjR0f3ODpECWMc7Y8im29Nr4uXuIt7tHcRSwmI6XxGhxqXkvlo\n496AaB0TTu+9++DzAZnz11bvHcEyWPLP5GdMGU9V3byBaLKdcxD3Zvmkd/+kyRCw\nPGEjbfY5AOj1zqu2UZheok/oCIz2CJnfQ05BGqblnf5WfhoorJAws0rubXkLiK8I\nVsZmL0fxAgMBAAECggEABNx+ccTGqGFljHvcUbas3iDoaP7tdpzbVmPz4OXhhltP\nKvTs51wku0IyGCs10ATSwnnWIuLJSSnlU7ZJ2Dl+9Moo1lbYGCh29Fm2+HRqwII/\nyoi3E8utSnk/wxVBJn2VNXwblYltw6WLoPI1vcYi4kniO7RqOUOo2TUBXH01/APZ\nRcB86Svw6Ia7+ViswxWEAdCELtFWipye3OVAcOwImjhN1GJHs3Onc0BygZqRJXfe\nTl9wCxHZgS5QT5ZrteLT65BT2RiPJeBAi2J9JujFMOpoGQBoM+pbA/x8iHa4aind\nlP3fnPsg/TCc5TZJ3IwquToDB1dvCRpWo+m6ZMfAJQKBgQD/mWB2D4D9C8QzI61v\nE3wva+vd/I53DzLRIr5TMuRvdf0nXRVwvsAAMn+E+HUzOpBfQJ3Kk6pExWUW50Fc\nGxQ/iZlklgPlVEJzUN2tOzyTatsFqX0QQGMVK9z/7yTe+yKYONL1ROBZFG6M4yTX\nn32FqdX9x36yxno8R/m0ZM/x7QKBgQDjUOwRybiMup1mmXh9hsMG6my6FbgDyXOh\nOiKQmvrlsTb3Ktp6SIaNyBwAdUzStuc1u4wEzlZobtt+ACWNEp3z9kLFK47pf0ap\n1v9oj83LXBqrduaoB+g7vRjVbfgsM0pbCW10xwXsjnck4z5wNBqFU3BtI5DU2kHJ\nSPtPdko9lQKBgQCXkozxdiA371JaQT4IMLXkKUumSK7zS8AG5WOYUwXEU2PchAbC\n5VtWwpt8bxqRVplm4xqvlwHR5n0cJ+dKh4RqaV7dl1iYFm+RktLid85kXWmk4e2Y\nRZZ8Z5aW72oeES9itc/kQwQHz2X/hnPCqoH1UdHkvPkVaz3xoX0izOXDwQKBgQCE\nZY6Jsb7+oHaq2np2SjZvYbygCaRa+EuTvUOCi/HUNIp6HYiQrotIKyQ8FBYBqKwz\n/J9J8VAclWzcD4PPjedXv7gWFQ+w6gOjSmkKYq+PYX7bHW6ssaZOnQ3IybtBK0KE\nkZIh8QV/SV8VqhGk0oQb4YRa3NsvTkwAy7QsDQ6inQKBgBJDs8FFkQzu4F3YHG55\npsHPXXN7O9ZUvLml9GmQMuFDFzqtuxDV/PHp0qt9hAF0UN62dlTTqrohtjmwbX2L\nY3ENkn4LcFhshB2ivwPBP5pEbxwWsDCusHqkYfUL0nC5qZdUGqx4qHmFjDC1HptY\nWr084Vi6tr48vfKeS1+U52QB\n-----END PRIVATE KEY-----\n",
#             "client_email": "marketr@marketr-app.iam.gserviceaccount.com",
#             "client_id": "103363973211179125545",
#             "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#             "token_uri": "https://oauth2.googleapis.com/token",
#             "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#             "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/marketr%40marketr-app.iam.gserviceaccount.com"
#             }
#         )
#         self.project_id = 'marketr-app'
        
#     def get(self, sql):
#         return pandas_gbq.read_gbq(sql, project_id=self.project_id)


# # In[31]:


# class GoogleORM(BigQuery):
#     def __init__(self, company_name):
#         super().__init__()
#         self.company_name = company_name.replace(" ", "_").lower()
        
#     def campaigns(self):
#         sql = f"""
#         SELECT *
#         FROM `{self.project_id}.{self.company_name}_adwords.campaigns`
#         """
        
        # return self.get(sql)


# In[32]:


# data = GoogleORM('musicmaker')
# df = data.campaigns()


# # In[33]:


# df.head()

