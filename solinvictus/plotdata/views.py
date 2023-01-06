# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
from .forms import LocalizationForm
from .models import Location
from .constants import OUTOFBOUND_MESSAGE
# Create your views here.

from geopy.geocoders import Nominatim
import folium
from folium.plugins import MousePosition
from jinja2 import Template


from django.contrib.auth.decorators import login_required

import json
import asyncio
import aiohttp
import logging
logging.basicConfig(level=logging.INFO)


fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"


def index(request, location_id=None):
    isSea = False
    if location_id:
        location = get_object_or_404(Location, pk=location_id)
        logging.info(f"""Redirected Index _ lat, lon, address: 
              {location.lat},
              {location.lon},
              {location.loc_description_text}""")
        zoom_start = 14
        if location.loc_description_text.startswith("[SEA?]"):
            zoom_start = 6
            pvdata = None
            isSea = True
        else:
            pvdata = asyncio.run(request_pvcalc_api(location))['outputs']['monthly']['fixed'][:2]
            with open("pvdata00.json", "w") as outfile:
                json.dump(pvdata, outfile)
            logging.info(pvdata)
    else:
        # get default location id=1
        location = get_object_or_404(Location, pk=1)
        print("Index_ lat, lon, address:",
              location.lat,
              location.lon,
              location.loc_description_text)
        zoom_start = 6
        pvdata = None

    map = folium.Map(
        location=[location.lat, location.lon],
        zoom_start=zoom_start,
        width=600, height=500)
    folium.Marker(location=[
        location.lat,
        location.lon]).add_to(map)
    MousePosition(
        position="topright",
        separator=" | ",
        prefix="Mouse:",
        lat_formatter=fmtr,
        lng_formatter=fmtr,
    ).add_to(map)
    click_c = folium.ClickForMarker()
    click_c._template = Template(
        '''
        {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                console.log("hola", {{this.get_name()}})
                function latLngPop(e) {
                    console.log("new", e.latlng)
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent(">Latitude: " + e.latlng.lat.toFixed(4) +
                                    "<br>Longitude: " + e.latlng.lng.toFixed(4)
                                    )
                        .openOn({{this._parent.get_name()}});
                        document.getElementById("id_latitude").value =
                                                e.latlng.lat.toFixed(4);
                        document.getElementById("id_longitude").value =
                                                e.latlng.lng.toFixed(4);
                        document.getElementById("loc_address").innerText =
                                                    "...";
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
                
        {% endmacro %}
        ''')

    map.add_child(click_c)
    # map.add_child(folium.LatLngPopup())
    # map.add_child(folium.ClickForMarker())
    # map.add_child(folium.ClickForLatLng(alert=False))
    # Save the map to a variable
    map_html = map.get_root().render()
    localization_form = LocalizationForm()
    localization_form.initial['latitude'] = location.lat
    localization_form.initial['longitude'] = location.lon
    if (location.is_within_limits()[0] & (not isSea)):
        return render(request,
                    'plotdata/index.html',
                    {
                        'location': location,
                        'map_html': map_html,
                        'pvdata': pvdata,
                        'localization_form': localization_form,
                    })
    else:
        return render(request,
                     'plotdata/index.html',
                        {'location': location,
                        'map_html': map_html,
                        'localization_form': localization_form,
                        'error_message': OUTOFBOUND_MESSAGE,
                        'pvdata': None,
                        })


@login_required
def list(request):
    location_list = Location.objects.all()
    template = loader.get_template('plotdata/list.html')
    context = {
        'location_list': location_list,
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("hello World. You are at the plotdata index")


def detail(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    geolocator = Nominatim(user_agent="my_application")
    geolocation = geolocator.reverse(f"{location.lat}, {location.lon}")
    print(geolocation.latitude, geolocation.longitude)
    map = folium.Map(
        location=[geolocation.latitude, geolocation.longitude],
        zoom_start=15)
    folium.Marker(location=[
        geolocation.latitude,
        geolocation.longitude]).add_to(map)
    # Save the map to a variable
    map_html = map.get_root().render()
    return render(request,
                  'plotdata/detail.html',
                  {
                    'location': location,
                    'geolocation': geolocation,
                    'map_html': map_html,
                  })

    # return HttpResponse("You're looking at location %s." % location_id)


def edit(request, location_id):
    print("EDIT VIEW ***********************")
    location = get_object_or_404(Location, pk=location_id)
    return render(request, 'plotdata/edit.html', {'location': location})


def save(request, location_id):
    print("save VIEW &&&&&&&&&&&&&&&&&&&&&&&&&")
    try:
        location = get_object_or_404(Location, pk=location_id)
        location.loc_description_text = request.POST['description']
        print("location from post object", location)
    except (KeyError, Location.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'plotdata/detail.html', {
            'location': location,
            'error_message': "You didn't select a location.",
        })
    else:
        location.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('plotdata:detail',
                                    args=(location_id,)))


def getLocation(request):
    print("get LOCATION.........")
    try:
        lat = request.POST['latitude']
        lon = request.POST['longitude']
        print(
            "location from post object: ",
            request.POST['latitude'],
            request.POST['longitude'])
        geolocator = Nominatim(user_agent="otj_aoo")
        geolocation = geolocator.reverse(f"{lat}, {lon}")
        address = geolocation.address

    except Exception as e:
        logging.error("Error in location API: ", e)
        address = "[SEA?] No address available for this location"

    finally:
        newlocation = Location.objects.create(
                                            lat=lat,
                                            lon=lon,
                                            loc_description_text=address
                                            )
        newlocation.save()
        return HttpResponseRedirect(
                                    reverse(
                                            'plotdata:index',
                                            args=(newlocation.pk,)
                                           )
                                    )


async def request_pvcalc_api(location, peakpower='1', systemloss='14'):
    def construct_url():
        # url example:
        # https://re.jrc.ec.europa.eu/api/v5_2/tool_name?param1=value1&param2=value2&...
        # 'https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?lat=39.57&lon=-5.15&peakpower=1&loss=14&outputformat=json'
        base = 'https://re.jrc.ec.europa.eu/api/v5_2/PVcalc?'
        latlon = f'lat={location.lat}&lon={location.lon}'
        power_and_loss = f'&peakpower={peakpower}&loss={systemloss}'
        outputformat = '&outputformat=json'
        return ''.join([base, latlon, power_and_loss, outputformat])
        
    # Make an asynchronous GET request to the API
    # Set the logging level to DEBUG
    # Log a message
    url = construct_url()
    logging.info(f'TRYING TO GET DATA FROM: {url}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Process the response
            data = await response.json()
            logging.info("data received...")
    return data


# ToDo
async def request_nominatum_api():
    async with Nominatim(
        user_agent="specify_your_app_name_here",
        adapter_factory=aiohttp.AioHTTPAdapter,
    ) as geolocator:
        location = await geolocator.geocode("175 5th Avenue NYC")
        print(location.address)
