from datetime import date
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Food, CustomerOrder, Reservation

def home(request):
    return render(request,"restaurant/home.html",{"foods":Food.objects.filter(is_available=True)[:6]})
def menu(request):
    foods=Food.objects.filter(is_available=True)
    category=request.GET.get("category","")
    if category: foods=foods.filter(category=category)
    return render(request,"restaurant/menu.html",{"foods":foods,"selected_category":category})
def cart(request):
    items=[]; total=0
    for fid, qty in request.session.get("cart",{}).items():
        try:
            food=Food.objects.get(pk=int(fid),is_available=True); qty=max(1,int(qty))
        except (Food.DoesNotExist,ValueError,TypeError): continue
        subtotal=food.price*qty; total+=subtotal; items.append({"food":food,"quantity":qty,"subtotal":subtotal})
    return render(request,"restaurant/cart.html",{"items":items,"total":total})
@require_POST
def add_to_cart(request,food_id):
    try: food=Food.objects.get(pk=food_id,is_available=True)
    except Food.DoesNotExist:
        messages.error(request,"料理が見つかりません。"); return redirect("menu")
    cart=request.session.get("cart",{}); cart[str(food.id)]=int(cart.get(str(food.id),0))+1; request.session["cart"]=cart
    messages.success(request,f"{food.name}をカートに追加しました。")
    return redirect(request.POST.get("next") or "menu")
@require_POST
def remove_from_cart(request,food_id):
    cart=request.session.get("cart",{}); cart.pop(str(food_id),None); request.session["cart"]=cart
    return redirect("cart")
def place_order(request):
    cart=request.session.get("cart",{}); lines=[]; total=0
    for fid,qty in cart.items():
        try: food=Food.objects.get(pk=int(fid),is_available=True); qty=max(1,int(qty))
        except (Food.DoesNotExist,ValueError,TypeError): continue
        lines.append(f"{food.name} × {qty} = ¥{food.price*qty}"); total+=food.price*qty
    if not lines: messages.info(request,"先にメニューから料理を選んでください。"); return redirect("menu")
    if request.method=="POST":
        name=request.POST.get("customer_name","").strip(); email=request.POST.get("email","").strip()
        if name and email:
            CustomerOrder.objects.create(customer_name=name,email=email,phone=request.POST.get("phone","").strip(),address=request.POST.get("address","").strip(),items_text="\n".join(lines),total=total)
            request.session["cart"]={}; messages.success(request,"ご注文を受け付けました。"); return redirect("home")
        messages.error(request,"名前とメールアドレスを入力してください。")
    return render(request,"restaurant/order.html",{"lines":lines,"total":total})
def reservation(request):
    if request.method=="POST":
        try:
            name=request.POST.get("customer_name","").strip(); email=request.POST.get("email","").strip(); phone=request.POST.get("phone","").strip()
            d=request.POST.get("reservation_date",""); t=request.POST.get("reservation_time",""); guests=int(request.POST.get("guests","2"))
            if not all([name,email,phone,d,t]) or date.fromisoformat(d)<date.today() or not 1<=guests<=30: raise ValueError
            Reservation.objects.create(customer_name=name,email=email,phone=phone,reservation_date=d,reservation_time=t,guests=guests,requests=request.POST.get("requests","").strip())
            messages.success(request,"ご予約を受け付けました。"); return redirect("reservation")
        except ValueError: messages.error(request,"入力を確認してください。予約日は今日以降、人数は1〜30人です。")
    return render(request,"restaurant/reservation.html")
def location(request): return render(request,"restaurant/location.html",{"geoapify_api_key":settings.GEOAPIFY_API_KEY})
def about(request): return render(request,"restaurant/about.html")
