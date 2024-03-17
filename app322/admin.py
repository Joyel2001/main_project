from django.contrib import admin

# Register your models here.


# main/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

from .models import Post, Like, Comment

from django.contrib import admin
from .models import Like

admin.site.register(Like)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'content', 'created_at')
    search_fields = ['post__title', 'content']
    list_filter = ('created_at',)


# company registeration
from .models import CompanyRegistration
admin.site.register(CompanyRegistration)


# seller_registertion

from .models import Seller
admin.site.register(Seller)


# tender 
from .models import Tender
admin.site.register(Tender)


# CompanyApplyForTender
from .models import CompanyApplyForTender
admin.site.register(CompanyApplyForTender)


from .models import ApprovedTender
admin.site.register(ApprovedTender)


from .models import RejectedTender
admin.site.register(RejectedTender)

from django.contrib import admin
from .models import Waste

admin.site.register(Waste)

from .models import Category

admin.site.register(Category)




from .models import Subcategory

admin.site.register(Subcategory)



from .models import Product

admin.site.register(Product)


from .models import Cart

admin.site.register(Cart)



from .models import Student

admin.site.register(Student)


from .models import Wishlist

admin.site.register(Wishlist)



# from .models import OrderItem

# admin.site.register(OrderItem)



from .models import Order

admin.site.register(Order)


from.models import ProductReview
admin.site.register(ProductReview)