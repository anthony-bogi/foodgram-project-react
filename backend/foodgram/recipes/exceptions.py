from django.http import HttpResponse

from .models import Ingredients


class MissingFontError(Exception):
    """
    Искллючение, если в системе отсутсвует опредленный шрифт для pdf.
    Тогда скачиваем файл в *.txt.
    """
    def generate_txt_shopping_list(self, ingredient_totals):
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        response.write("Список покупок\n\n")
        response.write("{}\n".format("=" * 20))
        for ingredient_name, ingredient_quantity in ingredient_totals.items():
            ingredient_unit = (
                Ingredients.objects.filter(ingredient__name=ingredient_name)
                .first()
                .ingredient.measurement_unit
            )
            response.write(
                "{}: {} {}\n".format(ingredient_name,
                                     ingredient_quantity,
                                     ingredient_unit)
            )
        return response
