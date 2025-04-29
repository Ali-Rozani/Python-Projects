import phonenumbers
from phonenumbers import geocoder, carrier
from rich.console import Console
from opencage.geocoder import OpenCageGeocode

console = Console()

geocoder_api = OpenCageGeocode("64a68360a8da4d6db3780888408467aa")

Phone_Number = "+92 03324572434"
Check_Phone_Number = phonenumbers.parse(Phone_Number)

Phone_Number_Location = geocoder.description_for_number(Check_Phone_Number, "en")
console.print("Phone Number Location:", Phone_Number_Location, style="bold green")

Phone_Number_Service_Provider = carrier.name_for_number(Check_Phone_Number, "en")
console.print("Phone Number Service Provider:", Phone_Number_Service_Provider, style="bold green")

Check_Valid_Phone_Number = phonenumbers.is_valid_number(Check_Phone_Number)
console.print("Is Phone Number Valid?:", Check_Valid_Phone_Number, style="bold green")

Check_Phone_Number_Region = geocoder.region_code_for_number(Check_Phone_Number)
console.print("Phone Number Region:", Check_Phone_Number_Region, style="bold green")

query = Phone_Number_Location
results = geocoder_api.geocode(query)

if results:
    latitude = results[0]["geometry"]["lat"]
    longitude = results[0]["geometry"]["lng"]
    console.print("Latitude:", latitude, style="bold green")
    console.print("Longitude:", longitude, style="bold green")
else:
    console.print("Could not find location data.", style="bold red")