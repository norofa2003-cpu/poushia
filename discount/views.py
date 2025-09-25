# discount/views.py
from django.shortcuts import redirect
from django.contrib import messages
from .models import DiscountCode
from poushia_order.models import Order

def apply_discount(request):
    if request.method == 'POST':
        code_input = request.POST.get('discount_code')
        try:
            discount = DiscountCode.objects.get(code=code_input)
            if discount.is_valid():
                # اعمال تخفیف روی سشن
                request.session['discount_percent'] = discount.discount_percent

                # افزایش شمارنده استفاده
                discount.used_count += 1
                discount.save()

                # ذخیره گزارش (اختیاری)
                open_order = Order.objects.filter(user_id=request.user.id, paid=False).first()
                if open_order:
                    # اگر مدل DiscountUsage ساختی، اینجا می‌تونی ذخیره‌اش کنی
                    pass  # یا DiscountUsage.objects.create(...)

                messages.success(request, f"کد تخفیف {discount.code} با {discount.discount_percent}% اعمال شد!")
            else:
                messages.error(request, "کد تخفیف منقضی شده، غیرفعال شده یا بیش از حد استفاده شده.")
        except DiscountCode.DoesNotExist:
            messages.error(request, "کد تخفیف نامعتبر است.")
    return redirect('order:cart')