import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import PokemonEntity, Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    list_data_pokemon_entities = PokemonEntity.objects.all()
    for pokemon_entity in list_data_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title_ru, request.build_absolute_uri(pokemon_entity.pokemon.image.url))

    list_data_pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in list_data_pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)

    list_entities = []
    for pokemon_entity in entities:
        list_entities.append({
            "level": pokemon_entity.level,
            "lat": pokemon_entity.lat,
            "lon": pokemon_entity.lon
        })
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            requested_pokemon.title_ru, request.build_absolute_uri(requested_pokemon.image.url))

    pokemon = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": requested_pokemon.image.url if requested_pokemon.image else DEFAULT_IMAGE_URL,
        "entities": list_entities
    }

    if requested_pokemon.next_evolutions:
        next_evolution = {
            "title_ru": requested_pokemon.next_evolutions.title_ru,
            "pokemon_id": requested_pokemon.next_evolutions.id,
            "img_url": requested_pokemon.next_evolutions.image.url if requested_pokemon.next_evolutions
                .image else DEFAULT_IMAGE_URL
        }
        pokemon.update({"next_evolution": next_evolution})

    if requested_pokemon.evolutions.all():
        previous_evolution = {
            "title_ru": requested_pokemon.evolutions.all()[0].title_ru,
            "pokemon_id": requested_pokemon.evolutions.all()[0].id,
            "img_url": requested_pokemon.evolutions.all()[0].image.url if requested_pokemon.evolutions.all()[0]
                .image else DEFAULT_IMAGE_URL
        }
        pokemon.update({"previous_evolution": previous_evolution})

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(), 'pokemon': pokemon})
