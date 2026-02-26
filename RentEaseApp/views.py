from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Offer, Photo, Conversation, Message, Favorite, Contract, ContractTemplate


def _format_price(value):
    """Format number with space as thousands separator (e.g. 3255 -> '3 255')."""
    if value is None:
        return ''
    try:
        n = int(value)
        return f'{n:,}'.replace(',', ' ')
    except (ValueError, TypeError):
        return str(value) if value else ''
from .forms import ContractPlaceholderForm

FIELD_LABELS = {}
for _cat, fields in ContractPlaceholderForm.get_field_groups():
    for fn, label in fields:
        FIELD_LABELS[fn] = label
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegisterForm, LoginForm, OfferForm, ProfileForm
from .models import LandlordUser, TenantUser
from django.http import HttpResponse, JsonResponse
from functools import wraps
from django.views.decorators.http import require_http_methods
import json
from django.db.models import Count
import json
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    pdfmetrics = None
    TTFont = None

from io import BytesIO
import os
import base64


def _register_pdf_fonts():
    """Register Unicode (DejaVu) fonts for PDF so Polish and other characters render. Returns (normal_font, bold_font)."""
    if not REPORTLAB_AVAILABLE or pdfmetrics is None or TTFont is None:
        return ('Helvetica', 'Helvetica-Bold')
    _base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sans_paths = [
        os.path.join(_base, 'static', 'fonts', 'DejaVuSans.ttf'),
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/TTF/DejaVuSans.ttf',
    ]
    bold_paths = [
        os.path.join(_base, 'static', 'fonts', 'DejaVuSans-Bold.ttf'),
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
    ]
    sans = next((p for p in sans_paths if os.path.isfile(p)), None)
    bold = next((p for p in bold_paths if os.path.isfile(p)), None)
    if sans:
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSans', sans))
            if bold:
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold))
            return ('DejaVuSans', 'DejaVuSans-Bold' if bold else 'DejaVuSans')
        except Exception:
            pass
    return ('Helvetica', 'Helvetica-Bold')


def get_logged_in_landlord(request):
    """Helper function to get the logged-in landlord user from session"""
    landlord_id = request.session.get('landlord_id')
    if landlord_id:
        try:
            return LandlordUser.objects.get(id=landlord_id)
        except LandlordUser.DoesNotExist:
            return None
    return None


def get_logged_in_tenant(request):
    """Helper function to get the logged-in tenant user from session"""
    tenant_id = request.session.get('tenant_id')
    if tenant_id:
        try:
            return TenantUser.objects.get(id=tenant_id)
        except TenantUser.DoesNotExist:
            return None
    return None


def landlord_required(view_func):
    """Decorator to require landlord login"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        landlord = get_logged_in_landlord(request)
        if not landlord:
            messages.error(request, "Please login as a landlord to access this page.")
            return redirect('login')
        request.landlord = landlord
        return view_func(request, *args, **kwargs)
    return wrapper


def mainSite(request):
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    assigned_offers = None
    if tenant:
        assigned_offers = Offer.objects.filter(assigned_user=tenant, status='Unavailable')
    
    offers = Offer.objects.exclude(status='Unavailable')
    price_from = request.GET.get('price_from', '')
    price_to = request.GET.get('price_to', '')
    area_from = request.GET.get('area_from', '')
    area_to = request.GET.get('area_to', '')
    rooms_from = request.GET.get('rooms_from', '')
    rooms_to = request.GET.get('rooms_to', '')
    year_from = request.GET.get('year_from', '')
    year_to = request.GET.get('year_to', '')
    admin_fees_from = request.GET.get('admin_fees_from', '')
    admin_fees_to = request.GET.get('admin_fees_to', '')
    deposit_from = request.GET.get('deposit_from', '')
    deposit_to = request.GET.get('deposit_to', '')
    rental_period_from = request.GET.get('rental_period_from', '')
    rental_period_to = request.GET.get('rental_period_to', '')
    sale_or_rent = request.GET.get('sale_or_rent', '')
    location = request.GET.get('location', '')
    floor = request.GET.get('floor', '')
    furnished = request.GET.get('furnished', '')
    condition = request.GET.get('condition', '')
    basement = request.GET.get('basement', '')
    balcony_terrace_garden = request.GET.get('balcony_terrace_garden', '')
    elevator = request.GET.get('elevator', '')
    heating = request.GET.get('heating', '')
    internet_fiber = request.GET.get('internet_fiber', '')
    pets_allowed = request.GET.get('pets_allowed', '')
    parking = request.GET.get('parking', '')
    building_type = request.GET.get('building_type', '')
    if price_from:
        try:
            offers = offers.filter(price__gte=int(price_from))
        except ValueError:
            pass
    if price_to:
        try:
            offers = offers.filter(price__lte=int(price_to))
        except ValueError:
            pass
    
    if area_from:
        try:
            offers = offers.filter(area__gte=int(area_from))
        except ValueError:
            pass
    if area_to:
        try:
            offers = offers.filter(area__lte=int(area_to))
        except ValueError:
            pass
    
    if rooms_from:
        try:
            offers = offers.filter(number_of_rooms__gte=int(rooms_from))
        except ValueError:
            pass
    if rooms_to:
        try:
            offers = offers.filter(number_of_rooms__lte=int(rooms_to))
        except ValueError:
            pass
    
    if year_from:
        try:
            offers = offers.filter(year_built__gte=int(year_from))
        except ValueError:
            pass
    if year_to:
        try:
            offers = offers.filter(year_built__lte=int(year_to))
        except ValueError:
            pass
    
    if admin_fees_from:
        try:
            offers = offers.filter(admin_fees__gte=int(admin_fees_from))
        except ValueError:
            pass
    if admin_fees_to:
        try:
            offers = offers.filter(admin_fees__lte=int(admin_fees_to))
        except ValueError:
            pass
    
    if deposit_from:
        try:
            offers = offers.filter(deposit__gte=int(deposit_from))
        except ValueError:
            pass
    if deposit_to:
        try:
            offers = offers.filter(deposit__lte=int(deposit_to))
        except ValueError:
            pass
    
    if rental_period_from:
        try:
            offers = offers.filter(minimum_rental_period__gte=int(rental_period_from))
        except ValueError:
            pass
    if rental_period_to:
        try:
            offers = offers.filter(minimum_rental_period__lte=int(rental_period_to))
        except ValueError:
            pass
    
    if sale_or_rent:
        offers = offers.filter(sale_or_rent=sale_or_rent)
    if location:
        offers = offers.filter(location__icontains=location)
    if floor:
        offers = offers.filter(floor=floor)
    if furnished:
        offers = offers.filter(furnished=furnished)
    if condition:
        offers = offers.filter(condition=condition)
    if basement:
        offers = offers.filter(basement=basement)
    if balcony_terrace_garden:
        offers = offers.filter(balcony_terrace_garden=balcony_terrace_garden)
    if elevator:
        offers = offers.filter(elevator=elevator)
    if heating:
        offers = offers.filter(heating=heating)
    if internet_fiber:
        offers = offers.filter(internet_fiber=internet_fiber)
    if pets_allowed:
        offers = offers.filter(pets_allowed=pets_allowed)
    if parking:
        offers = offers.filter(parking=parking)
    if building_type:
        offers = offers.filter(building_type=building_type)
    
    favorite_offer_ids = set()
    if tenant:
        favorite_offer_ids = set(
            Favorite.objects.filter(tenant=tenant)
            .values_list('offer_id', flat=True)
        )
    
    offers_list = list(offers)
    for offer in offers_list:
        offer.is_favorite = offer.id in favorite_offer_ids
    
    return render(request,"main_site.html", {
        "offers": offers_list,
        "landlord": landlord,
        "tenant": tenant,
        "assigned_offers": assigned_offers,
        "filter_params": request.GET
    })


def loginPanel(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = None
            user_type = None
            try:
                user = LandlordUser.objects.get(email=email)
                user_type = 'landlord'
            except LandlordUser.DoesNotExist:
                try:
                    user = TenantUser.objects.get(email=email)
                    user_type = 'tenant'
                except TenantUser.DoesNotExist:
                    user = None

            if user and check_password(password, user.password):
                if user_type == 'landlord':
                    request.session['landlord_id'] = user.id
                    request.session['user_type'] = 'landlord'
                    messages.success(request, f"Welcome {user.name}!")
                    return redirect('my_offers')
                else:
                    request.session['tenant_id'] = user.id
                    request.session['user_type'] = 'tenant'
                    messages.success(request, f"Welcome {user.name}!")
                    return redirect('offers')
            else:
                messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, "login_panel.html", {"form": form})


def logout(request):
    """Logout the current user"""
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('offers')


def registerPanel(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, "register_panel.html", {"form": form})


@landlord_required
def my_offers(request):
    """List all offers for the logged-in landlord"""
    landlord = request.landlord
    offers = Offer.objects.filter(user=landlord).order_by('-created_at')
    return render(request, "my_offers.html", {"offers": offers, "landlord": landlord})


@landlord_required
def create_offer(request):
    """Create a new offer"""
    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.landlord
            offer.save()
            
            photos = request.FILES.getlist('photos')
            for photo_file in photos:
                content = photo_file.read()
                photo_data = base64.b64encode(content).decode('utf-8')
                content_type = photo_file.content_type or 'image/jpeg'
                Photo.objects.create(offer=offer, photo_data=photo_data, content_type=content_type)
            
            messages.success(request, "Offer created successfully!")
            return redirect('my_offers')
    else:
        form = OfferForm()
    
    return render(request, "offer_form.html", {"form": form, "action": "Create", "landlord": request.landlord})


@landlord_required
def edit_offer(request, offer_id):
    """Edit an existing offer"""
    offer = get_object_or_404(Offer, id=offer_id, user=request.landlord)
    
    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            
            photos = request.FILES.getlist('photos')
            for photo_file in photos:
                content = photo_file.read()
                photo_data = base64.b64encode(content).decode('utf-8')
                content_type = photo_file.content_type or 'image/jpeg'
                Photo.objects.create(offer=offer, photo_data=photo_data, content_type=content_type)
            
            messages.success(request, "Offer updated successfully!")
            return redirect('my_offers')
    else:
        form = OfferForm(instance=offer)
    
    existing_photos = offer.photos.all()
    return render(request, "offer_form.html", {"form": form, "action": "Edit", "offer": offer, "existing_photos": existing_photos, "landlord": request.landlord})


@landlord_required
def delete_offer(request, offer_id):
    """Delete an offer"""
    offer = get_object_or_404(Offer, id=offer_id, user=request.landlord)
    
    if request.method == "POST":
        offer_title = offer.title
        offer.delete()
        messages.success(request, f"Offer '{offer_title}' deleted successfully!")
        return redirect('my_offers')
    
    return render(request, "delete_offer_confirm.html", {"offer": offer, "landlord": request.landlord})


def offer_detail(request, offer_id):
    """View offer details"""
    offer = get_object_or_404(Offer, id=offer_id)
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    is_owner = landlord and offer.user == landlord
    photos = offer.photos.all()
    
    conversation = None
    if tenant:
        conversation = Conversation.objects.filter(
            offer=offer,
            landlord=offer.user,
            tenant=tenant
        ).first()
    elif landlord and offer.user == landlord:
        conversations = Conversation.objects.filter(offer=offer, landlord=landlord)
        if conversations.exists():
            conversation = conversations.first()  
    
    is_favorite = False
    if tenant:
        is_favorite = Favorite.objects.filter(tenant=tenant, offer=offer).exists()
    
    return render(request, "offer_detail.html", {
        "offer": offer,
        "photos": photos,
        "landlord": landlord,
        "tenant": tenant,
        "is_owner": is_owner,
        "conversation": conversation,
        "is_favorite": is_favorite
    })


def tenant_required(view_func):
    """Decorator to require tenant login"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        tenant = get_logged_in_tenant(request)
        if not tenant:
            messages.error(request, "Please login as a tenant to access this page.")
            return redirect('login')
        request.tenant = tenant
        return view_func(request, *args, **kwargs)
    return wrapper


@require_http_methods(["GET", "POST"])
def conversations_list(request):
    """List all conversations for the logged-in user"""
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    
    if not landlord and not tenant:
        messages.error(request, "Please login to view conversations.")
        return redirect('login')
    
    if landlord:
        conversations = Conversation.objects.filter(
            landlord=landlord
        ).annotate(
            message_count=Count('messages')
        ).filter(
            message_count__gt=0
        ).order_by('-created_at')
        user_type = 'landlord'
    else:
        conversations = Conversation.objects.filter(
            tenant=tenant
        ).annotate(
            message_count=Count('messages')
        ).filter(
            message_count__gt=0
        ).order_by('-created_at')
        user_type = 'tenant'
    
    return render(request, "conversations_list.html", {
        "conversations": conversations,
        "user_type": user_type,
        "landlord": landlord,
        "tenant": tenant
    })


@require_http_methods(["GET", "POST"])
def conversation_detail(request, conversation_id):
    """View conversation details and send messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    
    if landlord:
        if conversation.landlord != landlord:
            messages.error(request, "You don't have access to this conversation.")
            return redirect('conversations_list')
        user_type = 'landlord'
        current_user = landlord
    elif tenant:
        if conversation.tenant != tenant:
            messages.error(request, "You don't have access to this conversation.")
            return redirect('conversations_list')
        user_type = 'tenant'
        current_user = tenant
    else:
        messages.error(request, "Please login to view conversations.")
        return redirect('login')
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                conversation=conversation,
                sender_id=current_user.id,
                sender_type=user_type,
                content=content
            )
            return redirect('conversation_detail', conversation_id=conversation_id)
    
    if user_type == 'landlord':
        conversation.messages.filter(sender_type='tenant').update(read_by_landlord=True)
    else:
        conversation.messages.filter(sender_type='landlord').update(read_by_tenant=True)
    
    messages_list = conversation.messages.all().order_by('created_at')
    
    return render(request, "conversation_detail.html", {
        "conversation": conversation,
        "messages": messages_list,
        "user_type": user_type,
        "landlord": landlord,
        "tenant": tenant,
        "current_user": current_user
    })


@require_http_methods(["GET", "POST"])
def conversation_detail_from_offer(request, offer_id):
    """View or create conversation from offer (lazy creation - only creates on first message)"""
    offer = get_object_or_404(Offer, id=offer_id)
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    
    if not tenant:
        messages.error(request, "Please login as a tenant to start a conversation.")
        return redirect('login')
    
    if landlord and offer.user == landlord:
        messages.error(request, "You cannot start a conversation about your own offer.")
        return redirect('offer_detail', offer_id=offer_id)
    
    if offer.status == 'Unavailable':
        messages.error(request, "This offer is no longer available.")
        return redirect('offer_detail', offer_id=offer_id)
    
    user_type = 'tenant'
    current_user = tenant
    conversation_landlord = offer.user
    
    conversation = Conversation.objects.filter(
        offer=offer,
        landlord=conversation_landlord,
        tenant=tenant
    ).first()
    
    if conversation:
        return redirect('conversation_detail', conversation_id=conversation.id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            conversation, created = Conversation.objects.get_or_create(
                offer=offer,
                landlord=conversation_landlord,
                tenant=tenant
            )
            
            Message.objects.create(
                conversation=conversation,
                sender_id=current_user.id,
                sender_type=user_type,
                content=content
            )
            
            return redirect('conversation_detail', conversation_id=conversation.id)
    
    from django.utils import timezone
    draft_conversation = type('DraftConversation', (), {
        'id': None,
        'offer': offer,
        'landlord': conversation_landlord,
        'tenant': tenant,
        'created_at': timezone.now()
    })()
    
    return render(request, "conversation_detail.html", {
        "conversation": draft_conversation,
        "messages": [],
        "user_type": user_type,
        "landlord": None,
        "tenant": tenant,
        "current_user": current_user,
        "is_draft": True,
        "offer_id": offer_id  
    })


@require_http_methods(["POST"])
def create_conversation(request, offer_id):
    """Create a conversation for an offer (backward compatibility - now redirects to draft mode)"""
    return redirect('conversation_detail_from_offer', offer_id=offer_id)


@require_http_methods(["POST"])
@landlord_required
def assign_tenant_to_offer(request, conversation_id):
    """Legacy endpoint - redirects to new rent_finalize"""
    return rent_finalize(request, conversation_id)


def get_notifications(request):
    """Get notification count and details for unread messages"""
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    
    if not landlord and not tenant:
        return JsonResponse({"unread_count": 0, "notifications": []})
    
    notifications = []
    unread_count = 0
    
    if landlord:
        conversations = Conversation.objects.filter(landlord=landlord)
        for conversation in conversations:
            unread_messages = conversation.messages.filter(
                read_by_landlord=False,
                sender_type='tenant'
            )
            count = unread_messages.count()
            if count > 0:
                unread_count += count
                notifications.append({
                    "conversation_id": conversation.id,
                    "offer_title": conversation.offer.title,
                    "offer_id": conversation.offer.id,
                    "tenant_name": f"{conversation.tenant.name} {conversation.tenant.surname}",
                    "unread_count": count,
                    "latest_message": unread_messages.last().content[:50] if unread_messages.last() else ""
                })
    elif tenant:
        conversations = Conversation.objects.filter(tenant=tenant)
        for conversation in conversations:
            unread_messages = conversation.messages.filter(
                read_by_tenant=False,
                sender_type='landlord'
            )
            count = unread_messages.count()
            if count > 0:
                unread_count += count
                notifications.append({
                    "conversation_id": conversation.id,
                    "offer_title": conversation.offer.title,
                    "offer_id": conversation.offer.id,
                    "landlord_name": f"{conversation.landlord.name} {conversation.landlord.surname}",
                    "unread_count": count,
                    "latest_message": unread_messages.last().content[:50] if unread_messages.last() else ""
                })
    
    return JsonResponse({
        "unread_count": unread_count,
        "notifications": notifications
    })


@require_http_methods(["POST"])
def mark_messages_as_read(request, conversation_id):
    """Mark all messages in a conversation as read"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    
    if landlord and conversation.landlord == landlord:
        conversation.messages.filter(sender_type='tenant').update(read_by_landlord=True)
    elif tenant and conversation.tenant == tenant:
        conversation.messages.filter(sender_type='landlord').update(read_by_tenant=True)
    else:
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    return JsonResponse({"success": True})


@require_http_methods(["GET", "POST"])
def profile(request):
    """View and edit user profile with conversations and assigned offers"""
    landlord = get_logged_in_landlord(request)
    tenant = get_logged_in_tenant(request)
    
    if not landlord and not tenant:
        messages.error(request, "Please login to view your profile.")
        return redirect('login')
    
    user = landlord or tenant
    user_type = 'landlord' if landlord else 'tenant'
    
    assigned_offers = None
    if tenant:
        assigned_offers = Offer.objects.filter(assigned_user=tenant, status='Unavailable')
    
    if landlord:
        conversations = Conversation.objects.filter(landlord=landlord).order_by('-created_at')
    else:
        conversations = Conversation.objects.filter(tenant=tenant).order_by('-created_at')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=user, user_type=user_type)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(user=user, user_type=user_type)
    
    return render(request, "profile.html", {
        "user": user,
        "user_type": user_type,
        "landlord": landlord,
        "tenant": tenant,
        "form": form,
        "assigned_offers": assigned_offers,
        "conversations": conversations
    })


@require_http_methods(["POST"])
def toggle_favorite(request, offer_id):
    """Toggle favorite status for an offer (API endpoint)"""
    tenant = get_logged_in_tenant(request)
    
    if not tenant:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    offer = get_object_or_404(Offer, id=offer_id)
    
    favorite, created = Favorite.objects.get_or_create(
        tenant=tenant,
        offer=offer
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return JsonResponse({
        "success": True,
        "isFavorite": is_favorite
    })


@require_http_methods(["GET"])
def get_favorites(request):
    """Get list of favorite offers for the current tenant (API endpoint)"""
    tenant = get_logged_in_tenant(request)
    
    if not tenant:
        return JsonResponse({"error": "Authentication required"}, status=401)
    
    favorites = Favorite.objects.filter(tenant=tenant).select_related('offer')
    favorite_offers = [fav.offer for fav in favorites]
    
    offers_data = []
    for offer in favorite_offers:
        first_photo = offer.photos.first()
        offers_data.append({
            "id": offer.id,
            "title": offer.title,
            "location": offer.location or "",
            "price": offer.price,
            "area": offer.area,
            "number_of_rooms": offer.number_of_rooms,
            "sale_or_rent": offer.sale_or_rent,
            "status": offer.status,
            "photo_url": first_photo.data_uri if first_photo else None,
            "created_at": offer.created_at.isoformat()
        })
    
    return JsonResponse({
        "success": True,
        "offers": offers_data
    })


@require_http_methods(["GET"])
def favorites_page(request):
    """Display favorites page for logged-in tenants"""
    tenant = get_logged_in_tenant(request)
    
    if not tenant:
        messages.error(request, "Please login to view your favorites.")
        return redirect('login')
    
    favorites = Favorite.objects.filter(tenant=tenant).select_related('offer')
    favorite_offers = [fav.offer for fav in favorites]
    
    return render(request, "favorites.html", {
        "offers": favorite_offers,
        "tenant": tenant
    })


@require_http_methods(["GET", "POST"])
@landlord_required
def create_contract(request, template_id=None):
    """Create a contract template (assigned to one or many offers)"""
    landlord = get_logged_in_landlord(request)
    
    available_offers = Offer.objects.filter(user=landlord).order_by('-created_at')
    
    template = None
    is_edit_mode = False
    if template_id:
        template = get_object_or_404(ContractTemplate, id=template_id, landlord=landlord)
        is_edit_mode = True
    
    preselected_offer_id = request.GET.get('offer_id')
    conversation_id = request.GET.get('conversation_id')
    
    if request.method == 'POST':
        template_content = request.POST.get('template_content', '')
        template_structure_json = request.POST.get('template_structure', '')
        selected_offer_ids = request.POST.getlist('offer_ids')
        
        if not template_content.strip() and not template_structure_json:
            messages.error(request, "Please enter contract template content.")
        elif not selected_offer_ids:
            messages.error(request, "Please select at least one offer.")
        else:
            template_structure = None
            if template_structure_json:
                try:
                    template_structure = json.loads(template_structure_json)
                except:
                    pass
            
            if template:
                template.template_content = template_content
                template.template_structure = template_structure if template_structure is not None else None
                template.save()
                template.offers.clear()
            else:
                template = ContractTemplate.objects.create(
                    landlord=landlord,
                    template_content=template_content,
                    template_structure=template_structure
                )
            
            selected_offers = Offer.objects.filter(id__in=selected_offer_ids, user=landlord)
            template.offers.set(selected_offers)
            
            if conversation_id and not is_edit_mode:
                try:
                    conversation = Conversation.objects.get(id=conversation_id, landlord=landlord)
                    offer = conversation.offer
                    tenant = conversation.tenant
                    
                    if offer in selected_offers:
                        final_content = generate_contract_from_template(template, offer, tenant, landlord)
                        
                        contract, created = Contract.objects.update_or_create(
                            offer=offer,
                            tenant=tenant,
                            landlord=landlord,
                            defaults={
                                'template': template,
                                'final_content': final_content
                            }
                        )
                        
                        offer.status = 'Unavailable'
                        offer.assigned_user = tenant
                        offer.save()
                        
                        Message.objects.create(
                            conversation=conversation,
                            sender_id=landlord.id,
                            sender_type='landlord',
                            content=f"📄 A contract has been generated for {offer.title}. Please review and sign the contract in your Contracts section."
                        )
                        
                        messages.success(request, f"Contract template created and contract generated for {tenant.name}! Notification sent.")
                        return redirect('conversation_detail', conversation_id=conversation_id)
                except Conversation.DoesNotExist:
                    pass
            
            if is_edit_mode:
                messages.success(request, f"Contract template updated and assigned to {selected_offers.count()} offer(s)!")
                return redirect('manage_contracts')
            else:
                messages.success(request, f"Contract template saved and assigned to {selected_offers.count()} offer(s)!")
                if conversation_id:
                    return redirect('conversation_detail', conversation_id=conversation_id)
                return redirect('create_contract')
    
    placeholder_form = ContractPlaceholderForm()
    field_groups = ContractPlaceholderForm.get_field_groups()
    
    tenant_fields = field_groups[0][1]  # (category, fields_list)
    landlord_fields = field_groups[1][1]
    property_fields = field_groups[2][1]
    
    return render(request, "contract_creator.html", {
        "landlord": landlord,
        "available_offers": available_offers,
        "template": template,
        "is_edit_mode": is_edit_mode,
        "preselected_offer_id": preselected_offer_id,
        "placeholder_form": placeholder_form,
        "tenant_fields": tenant_fields,
        "landlord_fields": landlord_fields,
        "property_fields": property_fields,
    })


@require_http_methods(["GET"])
@landlord_required
def manage_contracts(request):
    """Landlord dashboard to manage contract templates"""
    landlord = get_logged_in_landlord(request)
    templates = ContractTemplate.objects.filter(landlord=landlord).order_by('-created_at')
    generated_contracts = Contract.objects.filter(landlord=landlord).select_related('offer', 'tenant', 'template').order_by('-created_at')
    
    templates_with_preview = [(t, _get_template_preview_display(t)) for t in templates]
    return render(request, "manage_contracts.html", {
        "landlord": landlord,
        "templates_with_preview": templates_with_preview,
        "generated_contracts": generated_contracts
    })


@require_http_methods(["POST"])
@landlord_required
def delete_contract_template(request, template_id):
    """Delete a contract template"""
    landlord = get_logged_in_landlord(request)
    template = get_object_or_404(ContractTemplate, id=template_id, landlord=landlord)
    
    template.delete()
    messages.success(request, "Contract template deleted successfully.")
    return redirect('manage_contracts')


@require_http_methods(["GET"])
@tenant_required
def my_contracts(request):
    """Tenant dashboard to view their contracts"""
    tenant = get_logged_in_tenant(request)
    
    contracts = Contract.objects.filter(tenant=tenant).select_related('offer', 'landlord', 'template').order_by('-created_at')
    
    return render(request, "my_contracts.html", {
        "tenant": tenant,
        "contracts": contracts
    })


@require_http_methods(["GET"])
@tenant_required
def view_contract(request, contract_id):
    """View a specific contract (read-only)"""
    tenant = get_logged_in_tenant(request)
    contract = get_object_or_404(Contract, id=contract_id, tenant=tenant)
    
    return render(request, "view_contract.html", {
        "tenant": tenant,
        "contract": contract,
        "landlord": None
    })


@require_http_methods(["GET"])
@landlord_required
def view_contract_landlord(request, contract_id):
    """View a specific contract as landlord"""
    landlord = get_logged_in_landlord(request)
    contract = get_object_or_404(Contract, id=contract_id, landlord=landlord)
    
    return render(request, "view_contract.html", {
        "landlord": landlord,
        "contract": contract,
        "tenant": None
    })


@require_http_methods(["GET"])
def download_contract_pdf(request, contract_id):
    """Download contract as PDF"""
    if not REPORTLAB_AVAILABLE:
        back_url = request.build_absolute_uri(
            reverse('view_contract', args=[contract_id]) if get_logged_in_tenant(request)
            else reverse('view_contract_landlord', args=[contract_id])
        )
        html = (
            '<!DOCTYPE html><html><head><meta charset="utf-8"><title>PDF not available</title></head><body style="font-family:sans-serif;padding:2rem;">'
            '<h1>PDF download not available</h1>'
            '<p>Install the <code>reportlab</code> package to enable PDF export: <code>pip install reportlab</code></p>'
            f'<p><a href="{back_url}">Back to contract</a></p></body></html>'
        )
        return HttpResponse(html, content_type='text/html; charset=utf-8', status=503)

    tenant = get_logged_in_tenant(request)
    landlord = get_logged_in_landlord(request)

    if not tenant and not landlord:
        messages.error(request, "You must be logged in to download contracts.")
        return redirect('offers')

    if tenant:
        contract = get_object_or_404(Contract, id=contract_id, tenant=tenant)
    elif landlord:
        contract = get_object_or_404(Contract, id=contract_id, landlord=landlord)
    else:
        messages.error(request, "You don't have permission to download this contract.")
        return redirect('offers')

    if contract.template and contract.offer and contract.tenant and contract.landlord:
        contract_content = generate_contract_from_template(
            contract.template, contract.offer, contract.tenant, contract.landlord
        )
    else:
        contract_content = contract.final_content or (contract.template.template_content if contract.template else "")

    pdf_font, pdf_font_bold = _register_pdf_fonts()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)

    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1a1a1a',
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName=pdf_font_bold
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#1a1a1a',
        spaceAfter=12,
        spaceBefore=12,
        fontName=pdf_font_bold
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor='#1a1a1a',
        spaceAfter=12,
        leading=14,
        alignment=TA_JUSTIFY,
        fontName=pdf_font
    )

    title = Paragraph("Lease Agreement", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))

    meta_info = f"""
    <b>Property:</b> {contract.offer.title}<br/>
    <b>Location:</b> {contract.offer.location or 'N/A'}<br/>
    <b>Landlord:</b> {contract.landlord.name} {contract.landlord.surname}<br/>
    <b>Tenant:</b> {contract.tenant.name} {contract.tenant.surname}<br/>
    <b>Date Created:</b> {contract.created_at.strftime('%B %d, %Y')}<br/>
    """
    elements.append(Paragraph(meta_info, normal_style))
    elements.append(Spacer(1, 0.3*inch))

    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("<b>────────────────────────────────────────────────────────────</b>", normal_style))
    elements.append(Spacer(1, 0.2*inch))

    paragraphs = contract_content.split('\n')
    for para in paragraphs:
        para = para.strip()
        if para:
            para = ' '.join(para.split())
            para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            elements.append(Paragraph(para, normal_style))
            elements.append(Spacer(1, 0.1*inch))

    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("<b>────────────────────────────────────────────────────────────</b>", normal_style))
    elements.append(Spacer(1, 0.2*inch))

    signature_info = f"""
    <b>Signatures:</b><br/><br/>
    <b>Tenant:</b> {'✅ Signed' if contract.signed_by_tenant else '⏳ Pending'}
    """
    if contract.signed_by_tenant and contract.signed_by_tenant_at:
        signature_info += f" on {contract.signed_by_tenant_at.strftime('%B %d, %Y at %H:%M')}"
    signature_info += "<br/><br/>"

    signature_info += f"""
    <b>Landlord:</b> {'✅ Signed' if contract.signed_by_landlord else '⏳ Pending'}
    """
    if contract.signed_by_landlord and contract.signed_by_landlord_at:
        signature_info += f" on {contract.signed_by_landlord_at.strftime('%B %d, %Y at %H:%M')}"

    elements.append(Paragraph(signature_info, normal_style))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    safe_title = "".join(c if c.isalnum() or c in "._-" else "_" for c in contract.offer.title)[:50]
    filename = f"contract_{safe_title}_{contract.id}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response['Content-Length'] = len(pdf)

    return response


@require_http_methods(["POST"])
def sign_contract(request, contract_id, signer_type):
    """Sign a contract (tenant or landlord)"""
    from django.utils import timezone
    
    contract = get_object_or_404(Contract, id=contract_id)
    
    if signer_type == 'tenant':
        tenant = get_logged_in_tenant(request)
        if not tenant or contract.tenant != tenant:
            messages.error(request, "You don't have permission to sign this contract.")
            return redirect('my_contracts')
        
        contract.signed_by_tenant = True
        contract.signed_by_tenant_at = timezone.now()
        contract.save()
        
        conversation = Conversation.objects.filter(offer=contract.offer, tenant=tenant, landlord=contract.landlord).first()
        if conversation:
            Message.objects.create(
                conversation=conversation,
                sender_id=tenant.id,
                sender_type='tenant',
                content=f"✅ {tenant.name} {tenant.surname} has signed the contract for {contract.offer.title}."
            )
        
        messages.success(request, "Contract signed successfully!")
        return redirect('view_contract', contract_id=contract_id)
    
    elif signer_type == 'landlord':
        landlord = get_logged_in_landlord(request)
        if not landlord or contract.landlord != landlord:
            messages.error(request, "You don't have permission to sign this contract.")
            if landlord:
                return redirect('manage_contracts')
            else:
                return redirect('offers')
        
        contract.signed_by_landlord = True
        contract.signed_by_landlord_at = timezone.now()
        contract.save()
        
        conversation = Conversation.objects.filter(offer=contract.offer, tenant=contract.tenant, landlord=landlord).first()
        if conversation:
            Message.objects.create(
                conversation=conversation,
                sender_id=landlord.id,
                sender_type='landlord',
                content=f"✅ {landlord.name} {landlord.surname} has signed the contract for {contract.offer.title}."
            )
        
        messages.success(request, "Contract signed successfully!")
        return redirect('view_contract_landlord', contract_id=contract_id)
    
    return redirect('offers')


def _get_template_preview_display(template):
    """Build a human-readable preview string (with [Label] for placeholders) for manage_contracts."""
    if not template:
        return ""
    if template.template_structure:
        parts = []
        for item in template.template_structure:
            if item.get("type") == "text":
                parts.append(item.get("content", ""))
            elif item.get("type") == "block":
                label = item.get("label") or FIELD_LABELS.get(item.get("field_name", ""), item.get("field_name", ""))
                parts.append(f"[{label}]")
        return "".join(parts)
    content = template.template_content or ""
    for field_name, label in FIELD_LABELS.items():
        content = content.replace("{{" + field_name + "}}", f"[{label}]")
    return content


def _build_preview_content_with_labels(template_content, template_structure, landlord=None, offer=None):
    """Build content with placeholders as [Label] for manage_contracts display. Uses structure if available."""
    if template_structure:
        parts = []
        for item in template_structure:
            if item.get("type") == "text":
                parts.append(item.get("content", ""))
            elif item.get("type") == "block":
                label = item.get("label") or FIELD_LABELS.get(item.get("field_name", ""), item.get("field_name", ""))
                parts.append(f"[{label}]")
        content = "".join(parts)
    else:
        content = template_content or ""
        for field_name, label in FIELD_LABELS.items():
            content = content.replace("{{" + field_name + "}}", f"[{label}]")
    if landlord:
        content = content.replace("**Email**", landlord.email or "[Email]")
        content = content.replace("**Phone**", landlord.phone_number or "[Phone]")
        content = content.replace("**Bank Account**", landlord.bank_account_number or "[Bank Account]")
    if offer:
        content = content.replace("**Location**", offer.location or "[Location]")
        content = content.replace("**Area**", str(offer.area) if offer.area else "[Area]")
        content = content.replace("**Rooms**", str(offer.number_of_rooms) if offer.number_of_rooms else "[Rooms]")
        content = content.replace("**Floor**", offer.floor or "[Floor]")
        content = content.replace("**Price**", _format_price(offer.price) if offer.price else "[Price]")
    return content


def _build_preview_content_for_pdf(template_content, template_structure, landlord, offer=None):
    """Build preview content for PDF: landlord and property with real data, tenant as [Label]."""
    if template_structure:
        parts = []
        for item in template_structure:
            if item.get("type") == "text":
                parts.append(item.get("content", ""))
            elif item.get("type") == "block":
                fn = item.get("field_name", "")
                label = item.get("label") or FIELD_LABELS.get(fn, fn)
                if fn.startswith("landlord_") and landlord:
                    val = get_placeholder_value(fn, None, None, landlord)
                    parts.append(val if val else f"[{label}]")
                elif fn.startswith("property_") and offer:
                    val = get_placeholder_value(fn, offer, None, landlord)
                    parts.append(val if val else f"[{label}]")
                else:
                    parts.append(f"[{label}]")
        return "".join(parts)
    content = template_content or ""
    for field_name, label in FIELD_LABELS.items():
        if field_name.startswith("tenant_"):
            content = content.replace("{{" + field_name + "}}", f"[{label}]")
        elif field_name.startswith("landlord_") and landlord:
            val = get_placeholder_value(field_name, None, None, landlord)
            content = content.replace("{{" + field_name + "}}", val or f"[{label}]")
        elif field_name.startswith("property_") and offer:
            val = get_placeholder_value(field_name, offer, None, landlord)
            content = content.replace("{{" + field_name + "}}", val or f"[{label}]")
        else:
            content = content.replace("{{" + field_name + "}}", f"[{label}]")
    if landlord:
        content = content.replace("**Email**", landlord.email or "[Email]")
        content = content.replace("**Phone**", landlord.phone_number or "[Phone]")
        content = content.replace("**Bank Account**", landlord.bank_account_number or "[Bank Account]")
    if offer:
        content = content.replace("**Location**", offer.location or "[Location]")
        content = content.replace("**Area**", str(offer.area) if offer.area else "[Area]")
        content = content.replace("**Rooms**", str(offer.number_of_rooms) if offer.number_of_rooms else "[Rooms]")
        content = content.replace("**Floor**", offer.floor or "[Floor]")
        content = content.replace("**Price**", _format_price(offer.price) if offer.price else "[Price]")
    return content


@require_http_methods(["POST"])
@landlord_required
def preview_contract(request):
    """Preview contract template with sample data"""
    landlord = get_logged_in_landlord(request)
    
    template_content = request.POST.get('template_content', '')
    offer_id = request.POST.get('offer_id')  
    
    if not template_content:
        return JsonResponse({"error": "Template content is required"}, status=400)
    
    offer = None
    if offer_id:
        offer = Offer.objects.filter(id=offer_id, user=landlord).first()
    
    preview_content = template_content
    
    preview_content = preview_content.replace('{{tenant_name}}', '[Tenant Name]')
    preview_content = preview_content.replace('{{tenant_surname}}', '[Tenant Surname]')
    preview_content = preview_content.replace('{{tenant_full_name}}', '[Tenant Full Name]')
    preview_content = preview_content.replace('{{tenant_pesel}}', '[PESEL]')
    preview_content = preview_content.replace('{{tenant_id_card}}', '[ID Card Number]')
    preview_content = preview_content.replace('{{tenant_address}}', '[Tenant Address]')
    preview_content = preview_content.replace('{{tenant_phone}}', '[Phone Number]')
    preview_content = preview_content.replace('{{tenant_email}}', '[Email]')
    preview_content = preview_content.replace('{{tenant_bank_account}}', '[Bank Account]')
    
    preview_content = preview_content.replace('{{landlord_name}}', landlord.name or '')
    preview_content = preview_content.replace('{{landlord_surname}}', landlord.surname or '')
    preview_content = preview_content.replace('{{landlord_full_name}}', f"{landlord.name} {landlord.surname}" or '')
    preview_content = preview_content.replace('{{landlord_pesel}}', landlord.pesel or '')
    preview_content = preview_content.replace('{{landlord_id_card}}', landlord.id_card_number or '')
    preview_content = preview_content.replace('{{landlord_address}}', landlord.get_full_address() or '')
    preview_content = preview_content.replace('{{landlord_phone}}', landlord.phone_number or '')
    preview_content = preview_content.replace('{{landlord_email}}', landlord.email or '')
    preview_content = preview_content.replace('{{landlord_bank_account}}', landlord.bank_account_number or '')
    
    if offer:
        preview_content = preview_content.replace('{{property_title}}', offer.title or '[Property Title]')
        preview_content = preview_content.replace('{{property_location}}', offer.location or '[Location]')
        preview_content = preview_content.replace('{{property_price}}', _format_price(offer.price) if offer.price else '[Price]')
        preview_content = preview_content.replace('{{property_area}}', str(offer.area) if offer.area else '[Area]')
        preview_content = preview_content.replace('{{property_rooms}}', str(offer.number_of_rooms) if offer.number_of_rooms else '[Rooms]')
        preview_content = preview_content.replace('{{property_floor}}', offer.floor or '[Floor]')
        preview_content = preview_content.replace('{{property_description}}', offer.body or '[Description]')
    else:
        preview_content = preview_content.replace('{{property_title}}', '[Property Title]')
        preview_content = preview_content.replace('{{property_location}}', '[Location]')
        preview_content = preview_content.replace('{{property_price}}', '[Price]')
        preview_content = preview_content.replace('{{property_area}}', '[Area]')
        preview_content = preview_content.replace('{{property_rooms}}', '[Rooms]')
        preview_content = preview_content.replace('{{property_floor}}', '[Floor]')
        preview_content = preview_content.replace('{{property_description}}', '[Description]')
    
    return JsonResponse({
        "success": True,
        "preview_content": preview_content
    })


@require_http_methods(["POST"])
@landlord_required
def preview_contract_pdf(request):
    """Download contract template preview as PDF - same layout as generated contract, landlord/property filled."""
    if not REPORTLAB_AVAILABLE:
        return JsonResponse({"error": "PDF export not available. Install reportlab: pip install reportlab"}, status=503)
    from datetime import date
    landlord = get_logged_in_landlord(request)
    template_content = request.POST.get("template_content", "")
    template_structure_json = request.POST.get("template_structure", "")
    offer_id = request.POST.get("offer_id", "")
    template_structure = None
    if template_structure_json:
        try:
            template_structure = json.loads(template_structure_json)
        except (ValueError, TypeError):
            pass
    if not template_content and not template_structure:
        return JsonResponse({"error": "No template content"}, status=400)
    offer = None
    if offer_id:
        offer = Offer.objects.filter(id=offer_id, user=landlord).first()
    preview_content = _build_preview_content_for_pdf(template_content, template_structure, landlord, offer)
    pdf_font, pdf_font_bold = _register_pdf_fonts()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Heading1"], fontSize=18, textColor="#1a1a1a",
        spaceAfter=30, alignment=TA_CENTER, fontName=pdf_font_bold
    )
    normal_style = ParagraphStyle(
        "CustomNormal", parent=styles["Normal"], fontSize=11, textColor="#1a1a1a",
        spaceAfter=12, leading=14, alignment=TA_JUSTIFY, fontName=pdf_font
    )
    elements = []
    elements.append(Paragraph("Lease Agreement", title_style))
    elements.append(Spacer(1, 0.3 * inch))
    prop_title = offer.title if offer else "[Property Title]"
    prop_location = (offer.location or "N/A") if offer else "[Location]"
    landlord_name = f"{landlord.name or ''} {landlord.surname or ''}".strip() or "[Landlord]"
    meta_info = f"""
    <b>Property:</b> {prop_title}<br/>
    <b>Location:</b> {prop_location}<br/>
    <b>Landlord:</b> {landlord_name}<br/>
    <b>Tenant:</b> [Tenant Name]<br/>
    <b>Date Created:</b> {date.today().strftime('%B %d, %Y')}<br/>
    """
    elements.append(Paragraph(meta_info, normal_style))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("<b>────────────────────────────────────────────────────────────</b>", normal_style))
    elements.append(Spacer(1, 0.2 * inch))
    for para in preview_content.split("\n"):
        para = para.strip()
        if para:
            para = " ".join(para.split())
            para = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(para, normal_style))
            elements.append(Spacer(1, 0.1 * inch))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph("<b>────────────────────────────────────────────────────────────</b>", normal_style))
    elements.append(Spacer(1, 0.2 * inch))
    signature_info = """
    <b>Signatures:</b><br/><br/>
    <b>Tenant:</b> [ ] Pending<br/><br/>
    <b>Landlord:</b> [ ] Pending
    """
    elements.append(Paragraph(signature_info, normal_style))
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="contract_template_preview.pdf"'
    response["Content-Length"] = len(pdf)
    return response


def get_placeholder_value(field_name, offer, tenant, landlord):
    """Get the actual value for a placeholder field"""
    LABEL_TO_FIELD = {
        'Email': 'landlord_email', 'Phone': 'landlord_phone', 'Bank Account': 'landlord_bank_account',
        'Location': 'property_location', 'Area': 'property_area', 'Rooms': 'property_rooms',
        'Floor': 'property_floor', 'Price': 'property_price', 'Description': 'property_description',
        'Property Title': 'property_title', 'Tenant Name PESEL': None,
    }
    if field_name in LABEL_TO_FIELD:
        mapped = LABEL_TO_FIELD[field_name]
        if mapped:
            field_name = mapped
        elif field_name == 'Tenant Name PESEL':
            return f"{tenant.name or ''} {tenant.surname or ''} {tenant.pesel or ''}".strip()
    
    if field_name == 'tenant_name':
        return tenant.name or ''
    elif field_name == 'tenant_surname':
        return tenant.surname or ''
    elif field_name == 'tenant_full_name':
        return f"{tenant.name} {tenant.surname}" or ''
    elif field_name == 'tenant_pesel':
        return tenant.pesel or ''
    elif field_name == 'tenant_id_card':
        return tenant.id_card_number or ''
    elif field_name == 'tenant_address':
        return tenant.get_full_address() or ''
    elif field_name == 'tenant_phone':
        return tenant.phone_number or ''
    elif field_name == 'tenant_email':
        return tenant.email or ''
    elif field_name == 'tenant_bank_account':
        return tenant.bank_account_number or ''
    
    elif field_name == 'landlord_name':
        return landlord.name or ''
    elif field_name == 'landlord_surname':
        return landlord.surname or ''
    elif field_name == 'landlord_full_name':
        return f"{landlord.name} {landlord.surname}" or ''
    elif field_name == 'landlord_pesel':
        return landlord.pesel or ''
    elif field_name == 'landlord_id_card':
        return landlord.id_card_number or ''
    elif field_name == 'landlord_address':
        return landlord.get_full_address() or ''
    elif field_name == 'landlord_phone':
        return landlord.phone_number or ''
    elif field_name == 'landlord_email':
        return landlord.email or ''
    elif field_name == 'landlord_bank_account':
        return landlord.bank_account_number or ''
    
    elif field_name == 'property_title':
        return offer.title or ''
    elif field_name == 'property_location':
        return offer.location or ''
    elif field_name == 'property_price':
        return _format_price(offer.price)
    elif field_name == 'property_area':
        return str(offer.area) if offer.area else ''
    elif field_name == 'property_rooms':
        return str(offer.number_of_rooms) if offer.number_of_rooms else ''
    elif field_name == 'property_floor':
        return offer.floor or ''
    elif field_name == 'property_description':
        return offer.body or ''
    
    return ''


def generate_contract_from_template(template, offer, tenant, landlord):
    """Generate a contract instance from a template by replacing placeholders"""
    if template.template_structure:
        content_parts = []
        for item in template.template_structure:
            if item.get('type') == 'text':
                content_parts.append(item.get('content', ''))
            elif item.get('type') == 'block':
                field_name = item.get('field_name', '')
                value = get_placeholder_value(field_name, offer, tenant, landlord)
                content_parts.append(value)
        return ''.join(content_parts)
    else:
        content = template.template_content
        
        content = content.replace('{{tenant_name}}', tenant.name or '')
        content = content.replace('{{tenant_surname}}', tenant.surname or '')
        content = content.replace('{{tenant_full_name}}', f"{tenant.name} {tenant.surname}" or '')
        content = content.replace('{{tenant_pesel}}', tenant.pesel or '')
        content = content.replace('{{tenant_id_card}}', tenant.id_card_number or '')
        content = content.replace('{{tenant_address}}', tenant.get_full_address() or '')
        content = content.replace('{{tenant_phone}}', tenant.phone_number or '')
        content = content.replace('{{tenant_email}}', tenant.email or '')
        content = content.replace('{{tenant_bank_account}}', tenant.bank_account_number or '')
        
        content = content.replace('{{landlord_name}}', landlord.name or '')
        content = content.replace('{{landlord_surname}}', landlord.surname or '')
        content = content.replace('{{landlord_full_name}}', f"{landlord.name} {landlord.surname}" or '')
        content = content.replace('{{landlord_pesel}}', landlord.pesel or '')
        content = content.replace('{{landlord_id_card}}', landlord.id_card_number or '')
        content = content.replace('{{landlord_address}}', landlord.get_full_address() or '')
        content = content.replace('{{landlord_phone}}', landlord.phone_number or '')
        content = content.replace('{{landlord_email}}', landlord.email or '')
        content = content.replace('{{landlord_bank_account}}', landlord.bank_account_number or '')
        
        content = content.replace('{{property_title}}', offer.title or '')
        content = content.replace('{{property_location}}', offer.location or '')
        content = content.replace('{{property_price}}', _format_price(offer.price))
        content = content.replace('{{property_area}}', str(offer.area) if offer.area else '')
        content = content.replace('{{property_rooms}}', str(offer.number_of_rooms) if offer.number_of_rooms else '')
        content = content.replace('{{property_floor}}', offer.floor or '')
        content = content.replace('{{property_description}}', offer.body or '')
        
        content = content.replace('**Email**', landlord.email or '')
        content = content.replace('**Phone**', landlord.phone_number or '')
        content = content.replace('**Bank Account**', landlord.bank_account_number or '')
        content = content.replace('{{Email}}', landlord.email or '')
        content = content.replace('{{Phone}}', landlord.phone_number or '')
        content = content.replace('{{Bank Account}}', landlord.bank_account_number or '')
        tenant_name_pesel = f"{tenant.name or ''} {tenant.surname or ''} {tenant.pesel or ''}".strip()
        content = content.replace('**Tenant Name PESEL**', tenant_name_pesel)
        content = content.replace('{{Tenant Name PESEL}}', tenant_name_pesel)
        content = content.replace('**Location**', offer.location or '')
        content = content.replace('**Area**', str(offer.area) if offer.area else '')
        content = content.replace('**Rooms**', str(offer.number_of_rooms) if offer.number_of_rooms else '')
        content = content.replace('**Floor**', offer.floor or '')
        content = content.replace('**Price**', _format_price(offer.price))
        content = content.replace('{{Location}}', offer.location or '')
        content = content.replace('{{Area}}', str(offer.area) if offer.area else '')
        content = content.replace('{{Rooms}}', str(offer.number_of_rooms) if offer.number_of_rooms else '')
        content = content.replace('{{Floor}}', offer.floor or '')
        content = content.replace('{{Price}}', _format_price(offer.price))
        
        return content


@require_http_methods(["POST"])
@landlord_required
def rent_finalize(request, conversation_id):
    """Finalize rental - check for contract template and generate contract"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    landlord = get_logged_in_landlord(request)
    
    if conversation.landlord != landlord:
        messages.error(request, "You don't have permission to finalize this offer.")
        return redirect('conversations_list')
    
    offer = conversation.offer
    tenant = conversation.tenant
    
    contract_template = ContractTemplate.objects.filter(
        offers=offer,
        landlord=landlord
    ).first()
    
    if contract_template:
        final_content = generate_contract_from_template(contract_template, offer, tenant, landlord)
        
        contract, created = Contract.objects.update_or_create(
            offer=offer,
            tenant=tenant,
            landlord=landlord,
            defaults={
                'template': contract_template,
                'final_content': final_content
            }
        )
        
        offer.status = 'Unavailable'
        offer.assigned_user = tenant
        offer.save()
        
        Message.objects.create(
            conversation=conversation,
            sender_id=landlord.id,
            sender_type='landlord',
            content=f"📄 A contract has been generated for {offer.title}. Please review and sign the contract in your Contracts section."
        )
        
        messages.success(request, f"Contract generated and offer finalized! Notification sent to {tenant.name}.")
        return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        return JsonResponse({
            "has_template": False,
            "offer_id": offer.id,
            "conversation_id": conversation_id
        }, status=200)  


@require_http_methods(["POST"])
@landlord_required
def rent_finalize_external(request, conversation_id):
    """Finalize rental without digital contract (paper/external)"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    landlord = get_logged_in_landlord(request)
    
    if conversation.landlord != landlord:
        messages.error(request, "You don't have permission to finalize this offer.")
        return redirect('conversations_list')
    
    conversation.offer.status = 'Unavailable'
    conversation.offer.assigned_user = conversation.tenant
    conversation.offer.save()
    
    messages.success(request, f"Offer finalized. Assigned to {conversation.tenant.name} (external contract).")
    return redirect('conversation_detail', conversation_id=conversation_id)