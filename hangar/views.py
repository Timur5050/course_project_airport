import random
import requests

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator

from hangar.forms import (
    FlightSearchFormSource,
    AirplaneSearchForm,
    UserRegistrationForm,
    FlightSearchFormDestination,
    UserUpdateForm
)
from hangar.models import Airplane, User, Flight, Order, Ticket


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "hangar/index.html")


class UserCreationView(FormView):
    template_name = "hangar/user_form.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("hangar:main-page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "hangar/user_details.html"
    context_object_name = "user"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        orders = Order.objects.filter(user=user).select_related('user').prefetch_related('tickets__flight')

        paginator = Paginator(orders, self.paginate_by)
        page = self.request.GET.get('page')
        orders_page = paginator.get_page(page)

        context['orders'] = orders_page
        context['update_form'] = UserUpdateForm(instance=user)
        return context

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('hangar:user-profile', pk=user.pk)

        return self.get(request, *args, **kwargs)


class AirplaneListView(LoginRequiredMixin, ListView):
    model = Airplane
    template_name = "hangar/airplane_list.html"
    context_object_name = "airplane_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.GET.get("name")
        if search_name:
            queryset = queryset.filter(name__icontains=search_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = AirplaneSearchForm()
        return context


class AirplaneDetailView(LoginRequiredMixin, DetailView):
    model = Airplane
    context_object_name = "Airplane"
    template_name = "hangar/airplane_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        images = [
            "images/airplane_detail1.jpg",
            "images/airplane_detail2.jpg",
            "images/airplane_detail3.jpg",
        ]

        selected_image = random.choice(images)

        context['selected_image'] = selected_image
        return context


@login_required
def flight_list_view(request: HttpRequest) -> HttpResponse:
    queryset = Flight.objects.all()
    search_source = request.GET.get("source")
    destination = request.GET.get("destination")
    if search_source:
        queryset = queryset.filter(source__icontains=search_source)

    if destination:
        queryset = queryset.filter(destination__icontains=destination)

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "flight_list": page_obj,
        "search_form": FlightSearchFormSource(),
        "search_form_destination": FlightSearchFormDestination(),
        "page_obj": page_obj
    }
    return render(request, "hangar/flight_list.html", context=context)


class FlightDetailView(LoginRequiredMixin, DetailView):
    model = Flight
    context_object_name = "flight"
    template_name = "hangar/flight_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        booked_tickets = Ticket.objects.filter(flight=self.object)
        booked_seats = {(ticket.row, ticket.seat) for ticket in booked_tickets}

        cpp_server = "http://127.0.0.1:8080/post"
        data = {
            "rows": self.object.airplane.rows,
            "seats_per_row": self.object.airplane.seats_in_row,
            "booked_seats": list(booked_seats),
        }
        request = requests.post(cpp_server, json=data)

        result = [(i[0], i[1], False if i[2] == -2 else True) for i in request.json()["message"]]

        # rows = range(1, self.object.airplane.rows + 1)
        # seats_per_row = range(1, self.object.airplane.seats_in_row + 1)
        #
        # available_seats = [
        #     (row, seat, (row, seat) not in booked_seats)
        #     for row in rows
        #     for seat in seats_per_row
        # ]
        images = [
            "images/flight_detail1.jpg",
            "images/flight_detail2.jpg",
            "images/flight_detail3.jpg",
        ]
        selected_image = random.choice(images)
        # print(available_seats)
        context.update(
            {
                'available_seats': result,
                "selected_image": selected_image,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        flight = self.get_object()
        selected_seats = request.POST.getlist('seats')

        if not selected_seats:
            return self.get(request, *args, **kwargs)

        try:
            with transaction.atomic():
                order = Order.objects.create(user=request.user)
                for seat in selected_seats:
                    row, seat = map(int, seat.split('-'))
                    ticket = Ticket(
                        row=row,
                        seat=seat,
                        flight=flight,
                        order=order
                    )
                    ticket.save()

            return HttpResponseRedirect(reverse('hangar:flight-details', args=[flight.pk]))

        except ValidationError as e:
            return self.get(request, *args, **kwargs)
