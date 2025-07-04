import json

import pandas as pd
import requests

cookies = {
    'sb-login-auth-token.0': 'base64-eyJhY2Nlc3NfdG9rZW4iOiJleUpoYkdjaU9pSklVekkxTmlJc0ltdHBaQ0k2SW13MVNtNDNhalJwTHpGV00yWmFSMnNpTENKMGVYQWlPaUpLVjFRaWZRLmV5SnBjM01pT2lKb2RIUndjem92TDNoeVkyWmhhSEo2YTJwd1lteHRjbk5oYTI1NExuTjFjR0ZpWVhObExtTnZMMkYxZEdndmRqRWlMQ0p6ZFdJaU9pSTFNVEE1Wm1VNE1pMDBaak5rTFRRM1l6UXRPR0pqWkMwMFptSmxNelE0TlRGaU5qQWlMQ0poZFdRaU9pSmhkWFJvWlc1MGFXTmhkR1ZrSWl3aVpYaHdJam94TnpVeE9UYzNNak00TENKcFlYUWlPakUzTlRFek56STBORE1zSW1WdFlXbHNJam9pYW1KM1lXNW5NREV4TWtCbmJXRnBiQzVqYjIwaUxDSndhRzl1WlNJNklpSXNJbUZ3Y0Y5dFpYUmhaR0YwWVNJNmV5SndjbTkyYVdSbGNpSTZJbWR2YjJkc1pTSXNJbkJ5YjNacFpHVnljeUk2V3lKbmIyOW5iR1VpWFgwc0luVnpaWEpmYldWMFlXUmhkR0VpT25zaVlYWmhkR0Z5WDNWeWJDSTZJbWgwZEhCek9pOHZiR2d6TG1kdmIyZHNaWFZ6WlhKamIyNTBaVzUwTG1OdmJTOWhMMEZEWnpodlkweHNZWFpJV2pSNlJIQk5WVmxNUVhCSFVVUktTRmRCZHpSNVdrNTZVM1oxYjI1ck1XOXpjRXBmWTE5dmFVWnJaejF6T1RZdFl5SXNJbVZ0WVdsc0lqb2lhbUozWVc1bk1ERXhNa0JuYldGcGJDNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lablZzYkY5dVlXMWxJam9pNTQ2TDZaMlc1WTJhSWl3aWFYTnpJam9pYUhSMGNITTZMeTloWTJOdmRXNTBjeTVuYjI5bmJHVXVZMjl0SWl3aWJtRnRaU0k2SXVlT2ktbWRsdVdObWlJc0luQm9iMjVsWDNabGNtbG1hV1ZrSWpwbVlXeHpaU3dpY0dsamRIVnlaU0k2SW1oMGRIQnpPaTh2YkdnekxtZHZiMmRzWlhWelpYSmpiMjUwWlc1MExtTnZiUzloTDBGRFp6aHZZMHhzWVhaSVdqUjZSSEJOVlZsTVFYQkhVVVJLU0ZkQmR6UjVXazU2VTNaMWIyNXJNVzl6Y0VwZlkxOXZhVVpyWnoxek9UWXRZeUlzSW5CeWIzWnBaR1Z5WDJsa0lqb2lNVEEzTURNeE1qZzROVE0wTVRRME1EWTVORGd5SWl3aWMzVmlJam9pTVRBM01ETXhNamc0TlRNME1UUTBNRFk1TkRneUluMHNJbkp2YkdVaU9pSmhkWFJvWlc1MGFXTmhkR1ZrSWl3aVlXRnNJam9pWVdGc01TSXNJbUZ0Y2lJNlczc2liV1YwYUc5a0lqb2liMkYxZEdnaUxDSjBhVzFsYzNSaGJYQWlPakUzTlRFek56STBORE45WFN3aWMyVnpjMmx2Ymw5cFpDSTZJams1WkdVM00yUXpMV1poWldFdE5HUmtZaTFpWWpBMUxXUXhOV0l3TUdRMk9UVTFNaUlzSW1selgyRnViMjU1Ylc5MWN5STZabUZzYzJWOS5NeHlqRnhGMURjZlAzalNrOGdKSjFUZnZTdVdUaEhUY0MweW14SVJJa044IiwidG9rZW5fdHlwZSI6ImJlYXJlciIsImV4cGlyZXNfaW4iOjYwNDc5NSwiZXhwaXJlc19hdCI6MTc1MTk3NzIzOCwicmVmcmVzaF90b2tlbiI6Im95aTU3YXlheHg1dSIsInVzZXIiOnsiaWQiOiI1MTA5ZmU4Mi00ZjNkLTQ3YzQtOGJjZC00ZmJlMzQ4NTFiNjAiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJlbWFpbCI6Impid2FuZzAxMTJAZ21haWwuY29tIiwiZW1haWxfY29uZmlybWVkX2F0IjoiMjAyNS0wNy0wMVQxMjoyMDo0My4wNzM1NTRaIiwicGhvbmUiOiIiLCJjb25maXJtZWRfYXQiOiIyMDI1LTA3LTAxVDEyOjIwOjQzLjA3MzU1NFoiLCJsYXN0X3NpZ25faW5fYXQiOiIyMDI1LTA3LTAxVDEyOjIwOjQzLjYwNDI4MzI1M1oiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJ1c2VyX21ldGFkYXRhIjp7ImF2YXRhcl91cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMbGF2SFo0ekRwTVVZTEFwR1FESkhXQXc0eVpOelN2dW9uazFvc3BKX2Nfb2lGa2c9czk2LWMiLCJlbWFpbCI6Impid2FuZzAxMTJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6IueOi-mdluWNmiIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiLnjovpnZbljZoiLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMbGF2SFo0ekRwTVVZTEFwR1FESkhXQXc0eVpOelN2dW9uazFvc3BKX2Nfb2lGa2c9czk2LWMiLCJwcm92aWRlcl9pZCI6IjEwNzAzMTI4ODUzNDE0NDA2OTQ4MiIsInN1YiI6IjEwNzAzMTI4ODUzNDE0NDA2OTQ4MiJ9LCJpZGVudGl0aWVzIjpbeyJpZGVudGl0eV9pZCI6IjA3Njc1YTE3LTVlNTEtNGZkNS1hODFmLTUxZDViMDk5OWRkOSIsImlkIjoiMTA3MDMxMjg4NTM0MTQ0MDY5NDgyIiwidXNlcl9pZCI6IjUxMDlmZTgyLTRmM2QtNDdjNC04YmNkLTRmYmUzNDg1MWI2MCIsImlkZW50aXR5X2RhdGEiOnsiY',
    'sb-login-auth-token.1': 'XZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xsYXZIWjR6RHBNVVlMQXBHUURKSFdBdzR5Wk56U3Z1b25rMW9zcEpfY19vaUZrZz1zOTYtYyIsImVtYWlsIjoiamJ3YW5nMDExMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoi546L6Z2W5Y2aIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwibmFtZSI6IueOi-mdluWNmiIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xsYXZIWjR6RHBNVVlMQXBHUURKSFdBdzR5Wk56U3Z1b25rMW9zcEpfY19vaUZrZz1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTA3MDMxMjg4NTM0MTQ0MDY5NDgyIiwic3ViIjoiMTA3MDMxMjg4NTM0MTQ0MDY5NDgyIn0sInByb3ZpZGVyIjoiZ29vZ2xlIiwibGFzdF9zaWduX2luX2F0IjoiMjAyNS0wNy0wMVQxMjoyMDo0My4wNzAxOTJaIiwiY3JlYXRlZF9hdCI6IjIwMjUtMDctMDFUMTI6MjA6NDMuMDcwMjM3WiIsInVwZGF0ZWRfYXQiOiIyMDI1LTA3LTAxVDEyOjIwOjQzLjA3MDIzN1oiLCJlbWFpbCI6Impid2FuZzAxMTJAZ21haWwuY29tIn1dLCJjcmVhdGVkX2F0IjoiMjAyNS0wNy0wMVQxMjoyMDo0My4wNjUwMTVaIiwidXBkYXRlZF9hdCI6IjIwMjUtMDctMDFUMTI6MjA6NDMuNjA2ODkyWiIsImlzX2Fub255bW91cyI6ZmFsc2V9LCJwcm92aWRlcl90b2tlbiI6InlhMjkuYTBBUzNINk55aERPWEp2cXc5V3NjYUdjdi1aTkVsVGQ2c29uNE9sNGh1TDZ5al83b2R3eTh4dGwyd0g1ZkhZNDAtT1BoWFN5TVp2T292N0dSMG5EU1VldDF2aTRvcVM0eWFwakJpYlpGUUdjTmJwSEhQR2Q0S0p2OWx4NVU5cUF0OWdvWHNUX014MlNKc2hMTnZoU3l5WjFhR3dETTloYldxMEVHYW44RXVhQ2dZS0FaY1NBUkVTRlFIR1gyTWlKdDU0dElUTS1FcmZ1SUZZMXExQ193MDE3NSJ9',
    'ph_phc_POPg9pLdNURaPqBvYdOtOBO7tijCN3hQq7CGyoEbabd_posthog': '%7B%22distinct_id%22%3A%225109fe82-4f3d-47c4-8bcd-4fbe34851b60%22%2C%22%24sesid%22%3A%5B1751374423208%2C%220197c5ec-92d6-7b42-96a2-50b78824de42%22%2C1751372305110%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fpika.art%2Flogin%22%7D%7D',
}
headers = {
    'accept': 'text/x-component',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-type': 'text/plain;charset=UTF-8',
    'dnt': '1',
    'next-action': '806086efa9cf43973fd2875a9463d4318e204612',
    'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22(dashboard)%22%2C%7B%22children%22%3A%5B%22(featured)%22%2C%7B%22children%22%3A%5B%5B%22category%22%2C%22%22%2C%22oc%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2F%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
    'origin': 'https://pika.art',
    'priority': 'u=1, i',
    'referer': 'https://pika.art/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    # 'cookie': 'sb-login-auth-token.0=base64-eyJhY2Nlc3NfdG9rZW4iOiJleUpoYkdjaU9pSklVekkxTmlJc0ltdHBaQ0k2SW13MVNtNDNhalJwTHpGV00yWmFSMnNpTENKMGVYQWlPaUpLVjFRaWZRLmV5SnBjM01pT2lKb2RIUndjem92TDNoeVkyWmhhSEo2YTJwd1lteHRjbk5oYTI1NExuTjFjR0ZpWVhObExtTnZMMkYxZEdndmRqRWlMQ0p6ZFdJaU9pSTFNVEE1Wm1VNE1pMDBaak5rTFRRM1l6UXRPR0pqWkMwMFptSmxNelE0TlRGaU5qQWlMQ0poZFdRaU9pSmhkWFJvWlc1MGFXTmhkR1ZrSWl3aVpYaHdJam94TnpVeE9UYzNNak00TENKcFlYUWlPakUzTlRFek56STBORE1zSW1WdFlXbHNJam9pYW1KM1lXNW5NREV4TWtCbmJXRnBiQzVqYjIwaUxDSndhRzl1WlNJNklpSXNJbUZ3Y0Y5dFpYUmhaR0YwWVNJNmV5SndjbTkyYVdSbGNpSTZJbWR2YjJkc1pTSXNJbkJ5YjNacFpHVnljeUk2V3lKbmIyOW5iR1VpWFgwc0luVnpaWEpmYldWMFlXUmhkR0VpT25zaVlYWmhkR0Z5WDNWeWJDSTZJbWgwZEhCek9pOHZiR2d6TG1kdmIyZHNaWFZ6WlhKamIyNTBaVzUwTG1OdmJTOWhMMEZEWnpodlkweHNZWFpJV2pSNlJIQk5WVmxNUVhCSFVVUktTRmRCZHpSNVdrNTZVM1oxYjI1ck1XOXpjRXBmWTE5dmFVWnJaejF6T1RZdFl5SXNJbVZ0WVdsc0lqb2lhbUozWVc1bk1ERXhNa0JuYldGcGJDNWpiMjBpTENKbGJXRnBiRjkyWlhKcFptbGxaQ0k2ZEhKMVpTd2lablZzYkY5dVlXMWxJam9pNTQ2TDZaMlc1WTJhSWl3aWFYTnpJam9pYUhSMGNITTZMeTloWTJOdmRXNTBjeTVuYjI5bmJHVXVZMjl0SWl3aWJtRnRaU0k2SXVlT2ktbWRsdVdObWlJc0luQm9iMjVsWDNabGNtbG1hV1ZrSWpwbVlXeHpaU3dpY0dsamRIVnlaU0k2SW1oMGRIQnpPaTh2YkdnekxtZHZiMmRzWlhWelpYSmpiMjUwWlc1MExtTnZiUzloTDBGRFp6aHZZMHhzWVhaSVdqUjZSSEJOVlZsTVFYQkhVVVJLU0ZkQmR6UjVXazU2VTNaMWIyNXJNVzl6Y0VwZlkxOXZhVVpyWnoxek9UWXRZeUlzSW5CeWIzWnBaR1Z5WDJsa0lqb2lNVEEzTURNeE1qZzROVE0wTVRRME1EWTVORGd5SWl3aWMzVmlJam9pTVRBM01ETXhNamc0TlRNME1UUTBNRFk1TkRneUluMHNJbkp2YkdVaU9pSmhkWFJvWlc1MGFXTmhkR1ZrSWl3aVlXRnNJam9pWVdGc01TSXNJbUZ0Y2lJNlczc2liV1YwYUc5a0lqb2liMkYxZEdnaUxDSjBhVzFsYzNSaGJYQWlPakUzTlRFek56STBORE45WFN3aWMyVnpjMmx2Ymw5cFpDSTZJams1WkdVM00yUXpMV1poWldFdE5HUmtZaTFpWWpBMUxXUXhOV0l3TUdRMk9UVTFNaUlzSW1selgyRnViMjU1Ylc5MWN5STZabUZzYzJWOS5NeHlqRnhGMURjZlAzalNrOGdKSjFUZnZTdVdUaEhUY0MweW14SVJJa044IiwidG9rZW5fdHlwZSI6ImJlYXJlciIsImV4cGlyZXNfaW4iOjYwNDc5NSwiZXhwaXJlc19hdCI6MTc1MTk3NzIzOCwicmVmcmVzaF90b2tlbiI6Im95aTU3YXlheHg1dSIsInVzZXIiOnsiaWQiOiI1MTA5ZmU4Mi00ZjNkLTQ3YzQtOGJjZC00ZmJlMzQ4NTFiNjAiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJlbWFpbCI6Impid2FuZzAxMTJAZ21haWwuY29tIiwiZW1haWxfY29uZmlybWVkX2F0IjoiMjAyNS0wNy0wMVQxMjoyMDo0My4wNzM1NTRaIiwicGhvbmUiOiIiLCJjb25maXJtZWRfYXQiOiIyMDI1LTA3LTAxVDEyOjIwOjQzLjA3MzU1NFoiLCJsYXN0X3NpZ25faW5fYXQiOiIyMDI1LTA3LTAxVDEyOjIwOjQzLjYwNDI4MzI1M1oiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJ1c2VyX21ldGFkYXRhIjp7ImF2YXRhcl91cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMbGF2SFo0ekRwTVVZTEFwR1FESkhXQXc0eVpOelN2dW9uazFvc3BKX2Nfb2lGa2c9czk2LWMiLCJlbWFpbCI6Impid2FuZzAxMTJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6IueOi-mdluWNmiIsImlzcyI6Imh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbSIsIm5hbWUiOiLnjovpnZbljZoiLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMbGF2SFo0ekRwTVVZTEFwR1FESkhXQXc0eVpOelN2dW9uazFvc3BKX2Nfb2lGa2c9czk2LWMiLCJwcm92aWRlcl9pZCI6IjEwNzAzMTI4ODUzNDE0NDA2OTQ4MiIsInN1YiI6IjEwNzAzMTI4ODUzNDE0NDA2OTQ4MiJ9LCJpZGVudGl0aWVzIjpbeyJpZGVudGl0eV9pZCI6IjA3Njc1YTE3LTVlNTEtNGZkNS1hODFmLTUxZDViMDk5OWRkOSIsImlkIjoiMTA3MDMxMjg4NTM0MTQ0MDY5NDgyIiwidXNlcl9pZCI6IjUxMDlmZTgyLTRmM2QtNDdjNC04YmNkLTRmYmUzNDg1MWI2MCIsImlkZW50aXR5X2RhdGEiOnsiY; sb-login-auth-token.1=XZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xsYXZIWjR6RHBNVVlMQXBHUURKSFdBdzR5Wk56U3Z1b25rMW9zcEpfY19vaUZrZz1zOTYtYyIsImVtYWlsIjoiamJ3YW5nMDExMkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoi546L6Z2W5Y2aIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwibmFtZSI6IueOi-mdluWNmiIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xsYXZIWjR6RHBNVVlMQXBHUURKSFdBdzR5Wk56U3Z1b25rMW9zcEpfY19vaUZrZz1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTA3MDMxMjg4NTM0MTQ0MDY5NDgyIiwic3ViIjoiMTA3MDMxMjg4NTM0MTQ0MDY5NDgyIn0sInByb3ZpZGVyIjoiZ29vZ2xlIiwibGFzdF9zaWduX2luX2F0IjoiMjAyNS0wNy0wMVQxMjoyMDo0My4wNzAxOTJaIiwiY3JlYXRlZF9hdCI6IjIwMjUtMDctMDFUMTI6MjA6NDMuMDcwMjM3WiIsInVwZGF0ZWRfYXQiOiIyMDI1LTA3LTAxVDEyOjIwOjQzLjA3MDIzN1oiLCJlbWFpbCI6Impid2FuZzAxMTJAZ21haWwuY29tIn1dLCJjcmVhdGVkX2F0IjoiMjAyNS0wNy0wMVQxMjoyMDo0My4wNjUwMTVaIiwidXBkYXRlZF9hdCI6IjIwMjUtMDctMDFUMTI6MjA6NDMuNjA2ODkyWiIsImlzX2Fub255bW91cyI6ZmFsc2V9LCJwcm92aWRlcl90b2tlbiI6InlhMjkuYTBBUzNINk55aERPWEp2cXc5V3NjYUdjdi1aTkVsVGQ2c29uNE9sNGh1TDZ5al83b2R3eTh4dGwyd0g1ZkhZNDAtT1BoWFN5TVp2T292N0dSMG5EU1VldDF2aTRvcVM0eWFwakJpYlpGUUdjTmJwSEhQR2Q0S0p2OWx4NVU5cUF0OWdvWHNUX014MlNKc2hMTnZoU3l5WjFhR3dETTloYldxMEVHYW44RXVhQ2dZS0FaY1NBUkVTRlFIR1gyTWlKdDU0dElUTS1FcmZ1SUZZMXExQ193MDE3NSJ9; ph_phc_POPg9pLdNURaPqBvYdOtOBO7tijCN3hQq7CGyoEbabd_posthog=%7B%22distinct_id%22%3A%225109fe82-4f3d-47c4-8bcd-4fbe34851b60%22%2C%22%24sesid%22%3A%5B1751374423208%2C%220197c5ec-92d6-7b42-96a2-50b78824de42%22%2C1751372305110%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fpika.art%2Flogin%22%7D%7D',
}

videoUrllist = []
modellist = []
data = {}


def getVideoUrl(afterstr):
    global after
    bodydata = f'[{{"after":"{afterstr}","perPage":50,"category":"$undefined"}}]'
    response = requests.post('https://pika.art/', cookies=cookies, headers=headers, data=bodydata)
    raw_json_data = response.text[response.text.find("1:") + 2:]
    parsed_json = json.loads(raw_json_data)
    results = parsed_json['data']['results']
    for item in results:
        videoUrl = item.get('videoUrl')
        params = item.get('params', {})
        model = str(params.get('model'))
        if after == item.get('id'):
            break
        after = item.get('id')
        # print(f"{model} {videoUrl}")
        if model not in data:
            data[model] = []
        if len(data[model]) >= 200:
            print(f"{model} 的 URL 列表长度已达到或超过 200，跳过当前模型。")
            continue
        if videoUrl not in data[model]:
            data[model].append(videoUrl)
    return after  # 返回新的 after 值


if __name__ == '__main__':
    after = 'f6724f04-059e-4437-84ed-9caa61a72076'
    while True:
        after = getVideoUrl(after)
        print(after)
        # time.sleep(5)
        all_models_reached_200 = all(len(urls) >= 200 for urls in data.values())
        if all_models_reached_200:
            print("所有模型的 URL 列表长度都已达到或超过 200，退出程序。")
            break
        else:
            total_length = sum(len(urls) for urls in data.values())
            print(f"所有模型的 URL 列表总长度为：{total_length}")
        if after == "585c88c8-8a4e-4496-8873-1eb219bc052f":
            break
    print(data)
    for model in data.keys():
        df = pd.DataFrame(data[model])
        df.to_csv(f'第{model}.csv', index=False)
