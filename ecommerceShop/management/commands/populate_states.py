from django.core.management.base import BaseCommand
from ecommerceShop.models import State

class Command(BaseCommand):
    help = 'Populate the database with the 36 states of Nigeria'

    def handle(self, *args, **kwargs):
        # List of all 36 states in Nigeria
        states = [
            'Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue',
            'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe',
            'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara',
            'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau',
            'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara'
        ]

        # Default values for shipping fee and delivery availability
        shipping_fee = 1000.00  # Example fee, you can change it as needed
        delivery_available = False  # Example flag for delivery availability

        # Loop through the list of states and create a new State object for each
        for state_name in states:
            # Create and save each state
            state, created = State.objects.get_or_create(
                name=state_name,
                shipping_fee=shipping_fee,
                delivery_available=delivery_available
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created state: {state_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'State already exists: {state_name}'))

        self.stdout.write(self.style.SUCCESS('All states have been populated.'))
