from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Training


def trainings(request):
    trainings = Training.objects.order_by('date')

    # listing per pagina
    paginator = Paginator(trainings, 3)
    page = request.GET.get('page')
    paged_trainings = paginator.get_page(page)

    context = {
        'trainings': paged_trainings
    }
    return render(request, 'trainings.html', context)


def training(request, training_id):
    # Give Error if Listing ID not exist typed in URL
    training = get_object_or_404(Training, pk=training_id)

    context = {
        'training': training
    }

    return render(request, 'training.html', context)