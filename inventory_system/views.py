from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Products,Reservation
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
import json




from django.http import JsonResponse
from django.shortcuts import get_object_or_404
 # Import your model
def get_filtered_reservations(request):
    status = request.GET.get('status')  # Get the status parameter from the request
    user_id = request.GET.get('user_id')  # Get the user_id parameter from the request
    
    # Filter reservations based on status and user_id
    if status == 'All':
        reservations = Reservation.objects.filter(user_id=user_id)
    else:
        reservations = Reservation.objects.filter(status=status, user_id=user_id)
    
    # Serialize reservations data
    data = [{'id': reservation.id,
       'product_name': reservation.product_name,
             'quantity': reservation.quantity,
             'start_date': reservation.start_date,
             'end_date': reservation.end_date,
             'status': reservation.status,
             'product_image_url': reservation.product.image_url}
            for reservation in reservations]
    
    # Return JSON response
    return JsonResponse(data, safe=False)


def your_reservations(request):
    # Retrieve reservations for the logged-in user
    user_id = request.user.id
    reservations = Reservation.objects.filter(user_id=user_id)
    context = {'reservations': reservations}
    return render(request, 'inventory_system/YourReservations.html', context)
def handle_reservation_request(request):
    data = request.POST

    # Extract data from the request
    user_id = data.get('userId')
    username = data.get('username')
    quantity = data.get('quantity')
    product_name = data.get('productName')
    product_id = data.get('productId')
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    status = data.get('status')

    # Perform validation if necessary

    # Save reservation data in the database
    reservation = Reservation.objects.create(
        user_id=user_id,
        username=username,
        quantity=quantity,
        product_name=product_name,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
        status=status
    )

    # Return a JSON response
    return JsonResponse({'message': 'Reservation request received and saved successfully.'})
def remove_reservation(request, reservation_id):
    # Retrieve the reservation object
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Check if the reservation belongs to the current user
    if reservation.user_id != request.user.id:
        # Return unauthorized response or handle as appropriate
        return render(request, 'unauthorized.html')

    # Delete the reservation
    reservation.delete()
    
    # Redirect back to the reservations page
    return redirect('your_reservations')
def reservation_requests(request):
    # Retrieve all reservation requests from the database
    reservations = Reservation.objects.all()
    
    # Render the reservation requests template with the reservations data
    return render(request, 'adminReservationRequest.html', {'reservations': reservations})

def return_products(request, reservation_id):
    # Retrieve the reservation object
    reservation = Reservation.objects.get(id=reservation_id)
    
    # Update reservation status to Returned
    reservation.status = 'Reclaimed'
    reservation.save()
    
    # Retrieve the product related to the reservation
    product = reservation.product
    
    # Increase the quantity of the product by the reservation quantity
    product.quantity += reservation.quantity
    product.save()
    
    return JsonResponse({'message': 'Your return was processed Successfully.'})

def approve_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
  
    # Update reservation status to 'Approved'
    reservation.status = 'Approved'
    reservation.save()

    # Subtract quantity from product
    product_id = reservation.product_id
    product = get_object_or_404(Products, id=product_id)
    product.quantity -= reservation.quantity
    product.save()

    return redirect('reservation_requests')
def reject_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
  
    # Update reservation status to 'Rejected'
    reservation.status = 'Rejected'
    reservation.save()

    return redirect('reservation_requests')
def update_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, pk=product_id)
        product.name = request.POST.get('name')
        product.category = request.POST.get('category')
        product.quantity = request.POST.get('quantity')  # Changed from 'price' to 'quantity'
        product.availability = request.POST.get('availability')
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save(update_fields=['name', 'quantity', 'category', 'image', 'availability'])  # Updated fields list
        else:
            product.save(update_fields=['name', 'quantity', 'category', 'availability'])  # Updated fields list
        
        return JsonResponse({'success': True, 'message': 'Product updated successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')  # Changed from 'price' to 'quantity'
        availability = request.POST.get('availability')
        image = request.FILES.get('image')

        product = Products.objects.create(
          name=name,
          category=category,
          quantity=quantity,  # Changed from 'price' to 'quantity'
          image=image,
          availability=availability
        )
        product.save()
        return JsonResponse('Product added successfully', safe=False)
    else:
        return JsonResponse({'error': 'Product not added'})
    
def index(request):
  categories = ["All", "Computing Equipment", "Audio-Visual Equipment", 
                "Laboratory Equipment", "Workshop Tools", "Office Equipment", 
                "Educational and Teaching Aids", "Miscellaneous", "Available"
              ]

  products = Products.objects.all()
  context = {
    'products': products,
    'categories': categories
  }
  return render(request, "inventory_system/index.html", context)

def login_view(request):
  return render(request, "inventory_system/login.html")

def admin(request):
    return render(request, 'inventory_system/admin.html')

def login_user(request):
  data = json.loads(request.body)
  username=data['username']
  password=data['password']
  user = authenticate(request, username=username, password=password)
  print(user)
  # Check if authentication successful
  if user is not None:
    login(request, user)
    return JsonResponse("Login successful", safe=False)
  else:
    return JsonResponse("Invalid username or password.", safe=False)
  
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
  return render(request, "inventory_system/register.html")

@require_POST
def reclaim_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        product_id = reservation.product_id
        product = Products.objects.get(id=product_id)

        # Update product quantity and reservation status
        product.quantity += reservation.quantity
        product.save()

        reservation.status = 'Reclaimed'
        reservation.save()

        return JsonResponse({'message': 'Reservation reclaimed successfully.'})
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation does not exist.'}, status=404)
    except Products.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist.'}, status=404)
def registration(request):
  data = json.loads(request.body)
  username = data["username"]
  password = data["password"]
  confirmation = data["confirmation"]
  
  # Ensure password matches confirmation
  if password != confirmation:
    return JsonResponse("Passwords must match", safe=False)
  # Attempt to create new user
  try:
    user = User.objects.create_user(username, "" ,password)
    user.save()
    return JsonResponse("User created", safe=False)
  except IntegrityError:
    return JsonResponse("Username already taken", safe=False)
  
def search_view(request):
  categories = ["All", "Electronics", "Drugs", "Home Appliances", "Furniture", "Tech", "Books"]
  search = request.POST.get('search')
  products = Products.objects.filter(name__contains=search)
  context = {
    'products': products,
    'categories': categories
  }
  return render(request, "inventory_system/index.html", context)

def my_products_view(request):
    # Fetch all products from the database
    products = Products.objects.all()
    
    # Pass the products to the template
    context = {
        'products': products
    }

    return render(request, 'inventory_system/myproducts.html', context)
  
def edit_product_view(request, product_id):
  categories = ["Computing Equipment", "Audio-Visual Equipment", 
                "Laboratory Equipment", "Workshop Tools", "Office Equipment", 
                "Educational and Teaching Aids", "Miscellaneous"
              ]
  product = get_object_or_404(Products, id=product_id)
  context = {
      'product': product,
      'categories': categories
  }
  return render(request, 'inventory_system/edit_product.html', context)

def product_reservation(request, product_id):
  
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
     
        return redirect('index')  
    
    
    
    return render(request, 'inventory_system/reserve_product.html', {'product': product})

def delete_product_view(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    product.delete()
    return redirect('list_products')

def new_equipment(request):
  categories = ["Computing Equipment", "Audio-Visual Equipment", 
                "Laboratory Equipment", "Workshop Tools", "Office Equipment", 
                "Educational and Teaching Aids", "Miscellaneous"
              ]

  context = {
    'categories': categories
  }
  return render(request, "inventory_system/addproduct.html", context)