from django.shortcuts import render
from .models import *
# views.py in distance_app
import requests
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import THPT
import google.generativeai as genai
import re
import math
genai.configure(api_key="AIzaSyBLccnrIBeX4QpflJE1lKbSLleiv-MA6YA")
# Create your views here.
def home(request):
    districts = District.objects.all()
    subjects = Subject.objects.all()
    visitor_count, created = VisitorCount.objects.get_or_create(id=1)
    # Increment the count
    visitor_count.count += 1
    visitor_count.save()
    return render(request, 'index.html', {"districts": districts, 'subjects':subjects, 'visitor_count': visitor_count.count})



@csrf_exempt
def ans(request):
    if request.method == 'POST':
        loai_hinh = request.POST.get('loai-hinh', '')
        if loai_hinh == 'ts10-thuong':
            diem_toan = request.POST.get('diem-toan', '0')
            diem_ngu_van = request.POST.get('diem-ngu-van', '0')
            diem_ngoai_ngu = request.POST.get('diem-ngoai-ngu', '0')
            address = request.POST.get('address', '')
            quan = request.POST.get('quan', '')

            # Convert values to float if necessary
            diem_toan = float(diem_toan)
            diem_ngu_van = float(diem_ngu_van)
            diem_ngoai_ngu = float(diem_ngoai_ngu)
            nv1score = diem_ngu_van + diem_toan + diem_ngoai_ngu
            nv2score = nv1score - 3
            nv3score = nv1score - 6
            # Create a JSON response
            response_data = {
                'toan': diem_toan,
                'van': diem_ngu_van,
                'anh': diem_ngoai_ngu,
                'loai_hinh': loai_hinh,
                'address': address,
                'quan':quan
            }
            thpts = THPT.objects.all()
            arr_distance = []
            thpt_distances = []

            for thpt in thpts:
                distance = 0
                try:
                    response = requests.get(f'http://127.0.0.1:8000/calculate-distance/', params={'address1': address, 'address2': thpt.getaddress()})
                    distance = response.json().get('length')
                    distance = distance / 1000  # Convert meters to kilometers
                    distance = round(distance, 1)  # Round to one decimal place
                except:
                    distance = 100000
                arr_distance.append(distance)
                thpt_distances.append((thpt, distance))

            # Sort the list of THPT objects by distance
            thpt_distances.sort(key=lambda x: x[1])

            # Select the top 3 closest schools for nv1, nv2, and nv3 ensuring no duplicate schools between nv1, nv2, nv3
            nv1 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv1 <= nv1score and not thpt.isChuyen][:3]
            nv2 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv2 <= nv2score and not thpt.isChuyen and thpt not in [x[0] for x in nv1]][:3]
            nv3 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv3 <= nv3score and not thpt.isChuyen and thpt not in [x[0] for x in nv1 + nv2]][:3]

            # Print the distances and selected schools for nv1, nv2, nv3
            print("Distances: ", arr_distance)
            print("NV1: ", [(thpt.name, f"{distance} km") for thpt, distance in nv1])
            print("NV2: ", [(thpt.name, f"{distance} km") for thpt, distance in nv2])
            print("NV3: ", [(thpt.name, f"{distance} km") for thpt, distance in nv3])
             # Create the JSON response for nv1, nv2, nv3
            def format_nv(nv):
                return [{"name": thpt.name, "distance": f"{distance} km", "image": str(thpt.anh)} for thpt, distance in nv]

            nv1_json = json.dumps(format_nv(nv1), ensure_ascii=False)
            nv2_json = json.dumps(format_nv(nv2), ensure_ascii=False)   
            nv3_json = json.dumps(format_nv(nv3), ensure_ascii=False)

            return JsonResponse({'nv1s': nv1_json, 'nv2s': nv2_json, 'nv3s': nv3_json})
        if loai_hinh == 'ts10-chuyen':
            diem_toan = request.POST.get('diem-toan', '0')
            diem_ngu_van = request.POST.get('diem-ngu-van', '0')
            diem_ngoai_ngu = request.POST.get('diem-ngoai-ngu', '0')
            address = request.POST.get('address', '')
            quan = request.POST.get('quan', '')
            monchuyen = request.POST.get('mon-chuyen', '')
            diemchuyen = request.POST.get('diem-mon-chuyen', '')
            # mai làm tiếp =))
            # Convert values to float if necessary
            diem_toan = float(diem_toan)
            diem_ngu_van = float(diem_ngu_van)
            diem_ngoai_ngu = float(diem_ngoai_ngu)
            diemchuyen = float(diemchuyen)
            nv1score = diem_ngu_van + diem_toan + diem_ngoai_ngu + diemchuyen * 2
            nv2score = nv1score - 3
            # Create a JSON response
            thpts = THPT.objects.filter(monchuyen=monchuyen)
            arr_distance = []
            thpt_distances = []

            for thpt in thpts:
                distance = 0
                try:
                    response = requests.get(f'http://127.0.0.1:8000/calculate-distance/', params={'address1': address, 'address2': thpt.getaddress()})
                    distance = response.json().get('length')
                    distance = distance / 1000  # Convert meters to kilometers
                    distance = round(distance, 1)  # Round to one decimal place
                except:
                    distance = 100000
                arr_distance.append(distance)
                thpt_distances.append((thpt, distance))

            # Sort the list of THPT objects by distance
            thpt_distances.sort(key=lambda x: x[1])

            # Select the top 3 closest schools for nv1, nv2, and nv3 ensuring no duplicate schools between nv1, nv2, nv3
            nv1 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv1 <= nv1score and thpt.isChuyen][:1]
            nv2 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv2 <= nv2score and thpt.isChuyen and thpt not in [x[0] for x in nv1]][:1]

            # Print the distances and selected schools for nv1, nv2, nv3
            print("Distances: ", arr_distance)
            print("NV1: ", [(thpt.name, f"{distance} km") for thpt, distance in nv1])
            print("NV2: ", [(thpt.name, f"{distance} km") for thpt, distance in nv2])
             # Create the JSON response for nv1, nv2, nv3
            def format_nv(nv):
                return [{"name": thpt.name, "distance": f"{distance} km", "image": str(thpt.anh)} for thpt, distance in nv]

            nv1_json = json.dumps(format_nv(nv1), ensure_ascii=False)
            nv2_json = json.dumps(format_nv(nv2), ensure_ascii=False)   
            nv3_json = json.dumps(format_nv(nv2), ensure_ascii=False)   

            return JsonResponse({'nv1s': nv1_json, 'nv2s': nv2_json})
        if loai_hinh == 'ts10-tich-hop':
            diem_toan = request.POST.get('diem-toan', '0')
            diem_ngu_van = request.POST.get('diem-ngu-van', '0')
            diem_ngoai_ngu = request.POST.get('diem-ngoai-ngu', '0')
            address = request.POST.get('address', '')
            quan = request.POST.get('quan', '')
            diemtichhop = request.POST.get('diem-tichhop', '')
            # mai làm tiếp =))
            # Convert values to float if necessary
            diem_toan = float(diem_toan)
            diem_ngu_van = float(diem_ngu_van)
            diem_ngoai_ngu = float(diem_ngoai_ngu)
            diemtichhop = float(diemtichhop)
            nv1score = diem_ngu_van + diem_toan + diem_ngoai_ngu + diemtichhop
            nv2score = nv1score - 3
            nv3score = nv1score - 6
            # Create a JSON response
            thpts = THPT.objects.filter(monchuyen="Tích hợp")
            arr_distance = []
            thpt_distances = []

            for thpt in thpts:
                distance = 0
                try:
                    response = requests.get(f'http://127.0.0.1:8000/calculate-distance/', params={'address1': address, 'address2': thpt.getaddress()})
                    distance = response.json().get('length')
                    distance = distance / 1000  # Convert meters to kilometers
                    distance = round(distance, 1)  # Round to one decimal place
                except:
                    distance = 100000
                arr_distance.append(distance)
                thpt_distances.append((thpt, distance))

            # Sort the list of THPT objects by distance
            thpt_distances.sort(key=lambda x: x[1])

            # Select the top 3 closest schools for nv1, nv2, and nv3 ensuring no duplicate schools between nv1, nv2, nv3
            nv1 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv1 <= nv1score][:2]
            nv2 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv2 <= nv2score and thpt not in [x[0] for x in nv1]][:2]
            nv3 = [(thpt, distance) for thpt, distance in thpt_distances if thpt.nv3 <= nv3score and thpt not in [x[0] for x in nv1 + nv2]][:2]

            # Print the distances and selected schools for nv1, nv2, nv3
            print("Distances: ", arr_distance)
            print("NV1: ", [(thpt.name, f"{distance} km") for thpt, distance in nv1])
            print("NV2: ", [(thpt.name, f"{distance} km") for thpt, distance in nv2])
            print("NV3: ", [(thpt.name, f"{distance} km") for thpt, distance in nv3])
             # Create the JSON response for nv1, nv2, nv3
            def format_nv(nv):
                return [{"name": thpt.name, "distance": f"{distance} km", "image": str(thpt.anh)} for thpt, distance in nv]

            nv1_json = json.dumps(format_nv(nv1), ensure_ascii=False)
            nv2_json = json.dumps(format_nv(nv2), ensure_ascii=False)   
            nv3_json = json.dumps(format_nv(nv3), ensure_ascii=False)

            return JsonResponse({'nv1s': nv1_json, 'nv2s': nv2_json, 'nv3s': nv3_json})

    return JsonResponse({'hello':'hello'})



class DistanceView(View):
    def get(self, request):
        # Get the addresses from the query parameters, with defaults
        address1 = request.GET.get('address1', '')  # Default address
        address2 = request.GET.get('address2', '')  # Default address
        transport_mode = request.GET.get('transportMode', 'car')  # Default to car

        # Function to geocode an address
        def geocode(address):
            geocode_url = 'https://geocode.search.hereapi.com/v1/geocode'
            params = {
                'q': address,
                'apiKey': 'FKJdByW7d_QmFSdN8y8dF2f4x7pVNMHtgXb8O7Yr3So'
            }
            response = requests.get(geocode_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data['items']:
                return data['items'][0]['position']['lat'], data['items'][0]['position']['lng']
            else:
                return None  # Return None if no results found

        # Function to calculate the Haversine distance
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Radius of the Earth in km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c  # Distance in km

        # Geocode the addresses
        coords1 = geocode(address1)
        coords2 = geocode(address2)

        # Check if geocoding was successful
        if not coords1 or not coords2:
            return JsonResponse({'error': 'Geocoding failed for one or both addresses.'}, status=400)

        # Calculate the Haversine distance
        distance = haversine(coords1[0], coords1[1], coords2[0], coords2[1])

        # If the distance is greater than 10 km, return a response indicating the route exceeds the allowed distance
        if distance > 4.5:
            return JsonResponse({'error': 'far'}, status=500)

        # Construct the HERE API URL
        url = 'https://router.hereapi.com/v8/routes'
        params = {
            'transportMode': transport_mode,
            'origin': f"{coords1[0]},{coords1[1]}",
            'destination': f"{coords2[0]},{coords2[1]}",
            'return': 'summary',
            'apiKey': 'FKJdByW7d_QmFSdN8y8dF2f4x7pVNMHtgXb8O7Yr3So'  # Ensure this is set in your settings
        }

        try:
            # Make the request to the HERE API
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()  # Parse the JSON response

            # Extract the summary information
            route = data.get('routes', [{}])[0]  # Get the first route
            summary = route.get('sections', [{}])[0].get('summary', {})  # Get the summary of the first section

            # Return the summary as JSON
            return JsonResponse(summary)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

def text_to_html_paragraphs(text):
    # First, replace multiple newlines with a single newline,
    # so you don't get empty paragraphs
    text = re.sub(r'\n\s*\n', '\n', text)

    # Split the text into lines
    lines = text.split('\n')

    # Wrap each line in a <p> tag and join them
    return ''.join(f'{line.strip()}\n<br>' for line in lines)


def geminiview(request):
    return render(request, 'chat.html')

def gemini(request):
    text = request.GET.get('prompt')
    
    # Load training data from best.json
    with open('best.json', 'r', encoding='utf-8') as file:
        training_data = json.load(file)
    
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat()

    # Optionally, you can customize the input using the training data
    # For example, appending relevant data from the JSON to the input text
    text += "\nTraining Data:\n" + json.dumps(training_data, ensure_ascii=False, indent=2)
    
    response = chat.send_message(text)
    
    # Extract necessary data from response
    mess = text_to_html_paragraphs(response.text)
    
    return JsonResponse({"message": mess})