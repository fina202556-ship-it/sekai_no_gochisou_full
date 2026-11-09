from django.db import models
class Food(models.Model):
    CATEGORY_CHOICES = [("nepali","ネパール料理"),("japanese","日本料理"),("indian","インド料理"),("other","その他")]
    name = models.CharField("料理名", max_length=120)
    description = models.TextField("説明", blank=True)
    price = models.PositiveIntegerField("価格（円）")
    category = models.CharField("カテゴリー", max_length=20, choices=CATEGORY_CHOICES, default="other")
    image = models.ImageField("写真", upload_to="foods/", blank=True, null=True)
    is_available = models.BooleanField("販売中", default=True)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)
    class Meta:
        ordering = ["category", "name"]
        verbose_name = "料理"
        verbose_name_plural = "料理メニュー"
    def __str__(self): return f"{self.name} (¥{self.price})"

class CustomerOrder(models.Model):
    STATUS_CHOICES = [("new","新規"),("preparing","調理中"),("ready","準備完了"),("completed","完了"),("cancelled","キャンセル")]
    customer_name = models.CharField("お客様の名前", max_length=100)
    email = models.EmailField("メールアドレス")
    phone = models.CharField("電話番号", max_length=30, blank=True)
    address = models.CharField("住所", max_length=250, blank=True)
    items_text = models.TextField("注文内容")
    total = models.PositiveIntegerField("合計金額（円）", default=0)
    status = models.CharField("状態", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("注文日時", auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "注文"
        verbose_name_plural = "注文一覧"
    def __str__(self): return f"注文 #{self.pk} - {self.customer_name}"

class Reservation(models.Model):
    customer_name = models.CharField("お客様の名前", max_length=100)
    email = models.EmailField("メールアドレス")
    phone = models.CharField("電話番号", max_length=30)
    reservation_date = models.DateField("予約日")
    reservation_time = models.TimeField("予約時間")
    guests = models.PositiveSmallIntegerField("人数", default=2)
    requests = models.TextField("ご要望", blank=True)
    created_at = models.DateTimeField("受付日時", auto_now_add=True)
    class Meta:
        ordering = ["reservation_date", "reservation_time"]
        verbose_name = "予約"
        verbose_name_plural = "予約一覧"
    def __str__(self): return f"{self.customer_name} - {self.reservation_date} {self.reservation_time}"
