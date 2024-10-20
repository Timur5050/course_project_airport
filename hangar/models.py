from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return str(self.name)


class User(AbstractUser):
    pass


class Flight(models.Model):
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    duration = models.IntegerField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    distance = models.IntegerField(null=True, blank=True)
    flight_date = models.DateField()

    @property
    def new_name(self) -> str:
        return f"{self.source} -> {self.destination} ({self.flight_date})"

    def __str__(self):
        return f"{self.source} -> {self.destination} ({self.flight_date})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, flight):
        for ticket_attr_value, ticket_attr_name, flight_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            counter = getattr(flight, flight_attr_name)
            if not (1 <= ticket_attr_value <= counter):
                raise ValidationError(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number is not in range: (1, {counter})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert,
            force_update,
            using,
            update_fields)

    def __str__(self) -> str:
        return f"{self.row} {self.seat}"

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]
