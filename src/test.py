from services.zalo_client import ZaloClient


client = ZaloClient()


result = client.upload_images(['/home/daugau/Downloads/24991519_415057602244996_5228830774202876407_n.jpg'])
print(result)