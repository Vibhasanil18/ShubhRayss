from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import Event, Resource, Sweet, Sale,DiwaliWish,Diya,Question,Participant,UserDiwaliInfo,DiwaliCelebration
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import csv
import logging
from django.urls import reverse

#home
def home(request):
    return render(request, 'home.html')

# Register view
def register(request):
    context = {}

    if request.method == "GET":
        return render(request, 'register.html')
    else:
        un = request.POST['uname']
        p = request.POST['upass']
        cp = request.POST['ucpass']

        if un == "" or p == "" or cp == "":
            context['errmsg'] = 'Please fill all the fields'
        elif len(p) < 8:
            context['errmsg'] = 'Password must be at least 8 characters'
        elif p != cp:
            context['errmsg'] = 'Password & Confirm Password must be the same'
        else:
            try:
                # Create user without email integration
                u = User.objects.create(username=un)
                u.set_password(p)
                u.save()

                context['success'] = 'User Created Successfully.'
            except Exception as e:
                context['errmsg'] = f'Error: {str(e)}. User Already Exists.'

    return render(request, 'register.html', context)

# Login view
def user_login(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        un = request.POST['uname']
        p = request.POST['upass']
        u = authenticate(username=un, password=p)
        if u is not None:
            login(request, u)  # Log the user in
            return redirect('/home1')  # Redirect to home1 after login
        else:
            context['errmsg'] = "Invalid Credentials"
            return render(request, 'login.html', context)



# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, "You have been logged out.")  # Show logout success message
    return redirect(reverse('home'))  # Redirect to the landing page (home.html) after logout


# Home1 view (features page)
def home1(request):
    return render(request, 'home1.html')

@login_required
def festival_database(request):
    if request.method == 'POST':
        # Get data from the form
        region = request.POST.get('region')
        special_sweets = request.POST.get('special_sweets')
        celebration_description = request.POST.get('celebration_description')
        
        # Save to the database
        if region and special_sweets and celebration_description:
            DiwaliCelebration.objects.create(
                region=region,
                special_sweets=special_sweets,
                celebration_description=celebration_description
            )
            return redirect('festival_database')  # Redirect to avoid resubmitting form on refresh
    
    # Fetch all events from the database
    events = DiwaliCelebration.objects.all()
    return render(request, 'festival_database.html', {'events': events})

@login_required
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    participants = event.participants.all()
    resources = event.resources.all()

    return render(request, 'event_details.html', {
        'event': event,
        'participants': participants,
        'resources': resources,
    })

# Add or update sweets and track sales
@login_required
def sweet_shop(request):
    if request.method == "POST":
        # Handle adding a new sweet
        if 'add_sweet' in request.POST:
            # Retrieve input values from the POST request
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            image = request.FILES.get('image')  # Handle image upload (NEW)

            try:
                # Ensure price and stock are valid numbers
                price = float(price)
                stock = int(stock)
                
                # Create a new Sweet object with the uploaded image (if provided) (NEW)
                Sweet.objects.create(name=name, price=price, stock=stock, image=image)
                messages.success(request, "Sweet added successfully.")
            except ValueError:
                messages.error(request, "Invalid price or stock value.")

         # Handle updating inventory
        elif 'update_inventory' in request.POST:
            sweet_id = request.POST.get('sweet_id')
            stock = request.POST.get('stock')

            try:
                stock = int(stock)
                sweet = Sweet.objects.get(id=sweet_id)
                sweet.stock += stock
                sweet.save()
                messages.success(request, "Inventory updated successfully.")
            except ValueError:
                messages.error(request, "Invalid stock value.")
            except Sweet.DoesNotExist:
                messages.error(request, "Sweet not found.")

         # Handle selling a sweet (reducing stock)
        elif 'sell_sweet' in request.POST:
            sweet_id = request.POST.get('sweet_id')
            quantity = request.POST.get('quantity_sold')

            # Check if quantity is missing or invalid
            if not quantity or not quantity.isdigit():
                messages.error(request, "Please enter a valid quantity.")
                return redirect('sweet_shop')

            try:
                quantity = int(quantity)
                sweet = Sweet.objects.get(id=sweet_id)

                if sweet.stock >= quantity:
                    sweet.stock -= quantity
                    sweet.save()

                    # Save the sale record
                    sale = Sale.objects.create(sweet=sweet, quantity=quantity)
                    messages.success(request, f"Sold {quantity} of {sweet.name}.")
                else:
                    messages.error(request, "Not enough stock available.")
            except ValueError:
                messages.error(request, "Invalid quantity value.")
            except Sweet.DoesNotExist:
                messages.error(request, "Sweet not found.")

        return redirect('sweet_shop')  # Redirect after any operation

    # Fetch all sweets and sales data
    sweets = Sweet.objects.all()
    sales = Sale.objects.all()

    return render(request, 'sweet_shop.html', {'sweets': sweets, 'sales': sales})

# Generate and download the sales report as CSV
def download_sales_report(request):
    # Create a response object with 'csv' content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)
    writer.writerow(['Sweet Name', 'Quantity Sold', 'Sale Date'])  # Header row

    # Loop through each sale and write it to the CSV
    sales = Sale.objects.all()

    for sale in sales:
        writer.writerow([sale.sweet.name, sale.quantity, sale.sale_date])

    return response

# diwali wish page
@login_required
def create_wish(request):
    if request.method == "POST":
        name = request.POST.get('name')
        favorite_sweet = request.POST.get('favorite_sweet')

        if name and favorite_sweet:
            # Generate the personalized Diwali wish
            wish = f"Dear {name}, may your Diwali be as sweet as your favorite {favorite_sweet}! Wishing you joy, prosperity, and light this festive season."
            
            # Save the wish in the database
            diwali_wish = DiwaliWish(name=name, favorite_sweet=favorite_sweet, wish=wish)
            diwali_wish.save()

            # Add the wish to messages
            messages.success(request, wish)
        else:
            messages.error(request, "Please enter both your name and favorite sweet.")

    return render(request, 'create_wish.html')

#diya page
@login_required
def light_diyas(request):
    # Get all diyas from the database
    diyas = Diya.objects.all()

    # Count how many diyas are lit
    lit_count = Diya.objects.filter(status=True).count()

    # Render the template and pass the diyas and lit count
    return render(request, 'diya_map.html', {'diyas': diyas, 'lit_count': lit_count})

def toggle_diya(request, diya_id):
    # Get the diya by id
    diya = Diya.objects.get(id=diya_id)
    
    # Toggle the status (if it's unlit, light it; if it's lit, unlight it)
    diya.status = not diya.status
    diya.save()
    
    # After updating the status, redirect back to the light diyas page
    return redirect('light_diyas')


@login_required
def quiz_view(request):
    questions = Question.objects.all()  # Fetch all questions
    score = 0  # Initialize score variable
    
    if request.method == 'POST':
        # Debugging - print the POST data to ensure correct submission
        print("POST Data:", request.POST)

        # Loop through each question to compare the submitted answers
        for question in questions:
            # Get the selected answer for this question
            selected_answer = request.POST.get(f'question_{question.id}')
            
            # If no answer is selected, skip this question (or handle as desired)
            if selected_answer:
                # Convert both selected_answer and correct_answer to lowercase for comparison
                selected_answer = selected_answer.lower()  # Convert selected answer to lowercase
                correct_answer = question.correct_answer.lower()  # Convert correct answer to lowercase
                
                # Debugging - output selected answer and correct answer
                print(f"Question ID: {question.id}, Selected Answer: {selected_answer}, Correct Answer: {correct_answer}")
                
                if selected_answer == correct_answer:
                    score += 1  # Increment score if answer is correct

        total_questions = questions.count()  # Total number of questions
        return render(request, 'quiz_result.html', {'score': score, 'total': total_questions})

    return render(request, 'trivia_quiz.html', {'questions': questions})




