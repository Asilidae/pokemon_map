from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    title_ru = models.CharField(verbose_name='Название на русском языке',
                                max_length=200)
    title_en = models.CharField(verbose_name='Название на английском языке',
                                max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Название на японском языке',
                                max_length=200, blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='pokemons',
                              blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    next_evolutions = models.ForeignKey("Pokemon",
                                        on_delete=models.SET_NULL,
                                        verbose_name='В кого эволюционирует',
                                        blank=True,
                                        null=True,
                                        related_name='evolutions')

    def __str__(self):
        return '{title}'.format(title=self.title_ru)


class PokemonEntity(models.Model):
    """Координаты покемона"""
    pokemon = models.ForeignKey(Pokemon, verbose_name='Для какого покемона',
                                on_delete=models.CASCADE)
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Дата и время появления', null=True,
                                       blank=True)
    disappeared_at = models.DateTimeField('Дата и время исчезновения',
                                          null=True, blank=True)
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Здоровье', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return '{lat}; {lon}; {pokemon_title}' \
            .format(lat=self.lat,
                    lon=self.lon,
                    pokemon_title=self.pokemon.title_ru)
