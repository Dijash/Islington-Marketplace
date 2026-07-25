from django.core.management.base import BaseCommand
from Product.models import Category, Product


PRODUCTS = {
    'Clothes': [
        ('Classic White Oxford Shirt', 'A timeless white oxford shirt crafted from premium cotton. Perfect for formal and casual occasions alike.', 1299),
        ('Slim Fit Denim Jeans', 'Dark wash slim fit jeans with stretch comfort. A wardrobe essential for everyday style.', 1899),
        ('Printed Summer Dress', 'Lightweight floral print dress ideal for warm weather. Features a relaxed fit and vibrant colors.', 1599),
        ('Wool Blend Overcoat', 'Elegant wool blend overcoat for the colder months. Fully lined with a classic notch lapel.', 4999),
        ('Graphic Print Hoodie', 'Soft fleece hoodie with bold graphic print. Ribbed cuffs and kangaroo pocket for comfort.', 1499),
        ('Linen Blend Trousers', 'Breathable linen blend trousers with a tailored fit. Perfect for smart casual settings.', 1799),
        ('Leather Biker Jacket', 'Genuine leather biker jacket with asymmetric zip. A statement piece for any wardrobe.', 7999),
        ('Cotton Polo T-Shirt', 'Classic cotton polo shirt with a slim fit. Available in multiple colors for everyday wear.', 899),
        ('High-Waist Yoga Pants', 'Flexible high-waist yoga pants with moisture-wicking fabric. Great for workouts and lounging.', 1299),
        ('Plaid Flannel Shirt', 'Soft plaid flannel shirt in earthy tones. Button-down collar and chest pocket.', 1099),
        ('Track Suit Set', 'Matching zip-up jacket and jogger set. Lightweight polyester with mesh lining.', 2499),
    ],
    'Tech': [
        ('Wireless Bluetooth Earbuds', 'True wireless earbuds with active noise cancellation and 30-hour battery life.', 3499),
        ('Mechanical Gaming Keyboard', 'RGB backlit mechanical keyboard with hot-swappable switches and aluminum frame.', 4999),
        ('Portable Power Bank 20000mAh', 'High-capacity power bank with fast charging support and dual USB output ports.', 2299),
        ('Smart Fitness Watch', 'Track your health with heart rate monitoring, GPS, and 7-day battery life.', 5999),
        ('USB-C Hub Adapter 7-in-1', 'Multi-port adapter with HDMI, USB-A, SD card reader, and 100W power delivery.', 1899),
        ('Noise Cancelling Headphones', 'Over-ear headphones with premium ANC, 40-hour playback, and Hi-Res audio.', 7999),
        ('4K Webcam with Ring Light', 'Ultra HD webcam with built-in ring light and auto-focus for video calls.', 3299),
        ('Wireless Charging Pad', 'Sleek Qi-compatible wireless charger supporting up to 15W fast charge.', 999),
        ('Bluetooth Speaker Waterproof', 'IPX7 waterproof portable speaker with 360-degree sound and 12-hour battery.', 2799),
        ('Laptop Stand Adjustable', 'Ergonomic aluminum laptop stand with adjustable height and angle for better posture.', 1499),
        ('Smart LED Desk Lamp', 'Touch-control LED desk lamp with 5 brightness levels and USB charging port.', 1799),
    ],
    'Shoes': [
        ('Classic Canvas Sneakers', 'Lightweight canvas sneakers with rubber sole. Available in multiple colors.', 1299),
        ('Running Performance Shoes', 'Cushioned running shoes with breathable mesh upper and responsive foam sole.', 3499),
        ('Leather Chelsea Boots', 'Handcrafted leather Chelsea boots with elastic side panels and pull tab.', 4999),
        ('Sport Sandals', 'Adjustable sport sandals with arch support and non-slip rubber outsole.', 1499),
        ('Formal Derby Shoes', 'Polished leather derby shoes with Goodyear welt construction. Perfect for office wear.', 3999),
        ('High-Top Basketball Shoes', 'Ankle-supporting basketball shoes with air cushioning and durable traction.', 4499),
        ('Slip-On Loafers', 'Premium suede loafers with memory foam insole. Easy slip-on design for casual elegance.', 2299),
        ('Hiking Boots Waterproof', 'Waterproof hiking boots with ankle support and Vibram outsole for trail grip.', 5499),
        ('Platform Sneakers', 'Retro-style platform sneakers with chunky sole and premium leather upper.', 2799),
        ('Canvas Slip-On Vans', 'Classic canvas slip-ons with waffle outsole. Effortless style for everyday wear.', 1599),
    ],
    'Jewellery': [
        ('Sterling Silver Chain Necklace', 'Elegant sterling silver chain necklace with lobster clasp. 18-inch adjustable length.', 2499),
        ('Gold Plated Hoop Earrings', 'Minimalist gold plated hoop earrings with hypoallergenic posts.', 1299),
        ('Diamond Stud Earrings', '0.5 carat diamond stud earrings set in 14K white gold with secure butterfly backs.', 9999),
        ('Leather Strap Watch', 'Classic analog watch with genuine leather strap and stainless steel case.', 3499),
        ('Pearl Bracelet', 'Natural freshwater pearl bracelet with elastic cord. Elegant and timeless.', 1899),
        ('Men\'s Signet Ring', 'Sterling silver signet ring with personalized engraving option.', 1599),
        ('Layered Pendant Necklace', 'Gold layered necklace set with heart, star, and moon pendants.', 1799),
        ('Tennis Bracelet Cubic Zirconia', 'Sparkling cubic zirconia tennis bracelet set in rhodium-plated silver.', 2299),
        ('Anklet with Charms', 'Delicate gold anklet with adjustable chain and mix of charm pendants.', 999),
        ('Men\'s Titanium Ring', 'Brushed titanium band ring with beveled edge. Perfect for everyday wear.', 2199),
    ],
    'Home Appliances': [
        ('Robot Vacuum Cleaner', 'Smart robot vacuum with mapping, app control, and auto-charging capability.', 12999),
        ('Air Purifier HEPA', 'True HEPA air purifier covering up to 500 sq ft. Removes 99.97% of allergens.', 7999),
        ('Espresso Coffee Machine', 'Semi-automatic espresso machine with 15-bar pressure and milk frother.', 14999),
        ('Cordless Stick Vacuum', 'Lightweight cordless vacuum with powerful suction and detachable battery.', 8999),
        ('Electric Kettle 1.7L', 'Fast-boil electric kettle with temperature control and auto shut-off.', 1999),
        ('Blender 1200W', 'High-power blender for smoothies, soups, and ice crushing. 6 stainless blades.', 3499),
        ('Microwave Oven 25L', 'Convection microwave with 10 power levels, grill function, and digital display.', 9999),
        ('Standing Fan Quiet', 'Ultra-quiet 16-inch standing fan with 3 speed settings and oscillation.', 2999),
        ('Steam Iron 2400W', 'Powerful steam iron with ceramic soleplate and anti-drip technology.', 2499),
        ('Rice Cooker 5L', 'Multi-function rice cooker with digital controls and keep-warm feature.', 3999),
    ],
    'Alcohol': [
        ('Single Malt Whisky 12yr', 'Aged 12 years in oak casks. Rich notes of honey, vanilla, and subtle smokiness.', 5999),
        ('Craft Lager Beer 6-Pack', 'Crisp and refreshing craft lager brewed with imported hops. 330ml cans.', 1499),
        ('Red Wine Cabernet Sauvignon', 'Full-bodied Cabernet Sauvignon with dark fruit flavors and smooth tannins.', 2999),
        ('Premium Vodka 750ml', 'Triple-distilled premium vodka with a clean, smooth finish. Perfect for cocktails.', 3499),
        ('Gin London Dry 700ml', 'Classic London dry gin with juniper, citrus, and botanical notes.', 2799),
        ('Sparkling Prosecco', 'Italian prosecco with delicate bubbles and notes of green apple and pear.', 2299),
        ('Aged Rum 8yr', 'Caribbean rum aged 8 years in bourbon barrels. Rich caramel and spice notes.', 4499),
        ('Tequila Blanco 750ml', '100% agave blanco tequila. Crisp and clean with notes of citrus and pepper.', 3299),
        ('Irish Stout Beer 4-Pack', 'Smooth and creamy Irish stout with roasted barley and coffee undertones.', 1299),
        ('Bourbon Whiskey 750ml', 'Small-batch bourbon with notes of caramel, oak, and warm spice finish.', 4999),
    ],
    'Coffee': [
        ('Colombian Arabica Beans 1kg', 'Single-origin Colombian beans with bright acidity and chocolatey finish.', 1999),
        ('Espresso Roast Ground 500g', 'Dark roast ground coffee designed for espresso. Bold and intense flavor.', 1299),
        ('Cold Brew Concentrate 1L', 'Ready-to-drink cold brew concentrate. Smooth, low-acid, and refreshing.', 899),
        ('Instant Coffee Premium 200g', 'Premium freeze-dried instant coffee. Rich aroma and full-bodied taste.', 699),
        ('Coffee Pods Variety Pack', 'Compatible coffee pods with 5 different flavors. 40 pods total.', 1499),
        ('Green Coffee Beans 500g', 'Unroasted green coffee beans for home roasting. Rich in antioxidants.', 999),
        ('Flavored Ground Coffee Vanilla', 'Vanilla-flavored ground coffee with natural flavoring. Medium roast.', 799),
        ('Coffee Grinder Burr', 'Conical burr grinder with 35 grind settings for perfect extraction.', 3499),
        ('Ethiopian Yirgacheffe 500g', 'Light roast with floral and citrus notes. A specialty coffee classic.', 1599),
        ('Cold Brew Maker 1.5L', 'Borosilicate glass cold brew maker with stainless steel filter. Easy to use.', 1799),
    ],
    'Tea': [
        ('Darjeeling First Flush 250g', 'Premium first flush Darjeeling with muscatel flavor and floral aroma.', 1299),
        ('Green Tea Sencha 100 Bags', 'Japanese sencha green tea bags. Rich in antioxidants with a fresh taste.', 599),
        ('English Breakfast Loose Leaf', 'Classic English breakfast blend. Full-bodied and perfect with milk.', 799),
        ('Chamomile Herbal Tea 50 Bags', 'Soothing chamomile tea bags for relaxation. Caffeine-free and natural.', 499),
        ('Masala Chai Spice Blend', 'Authentic Indian masala chai blend with cardamom, cinnamon, and ginger.', 699),
        ('Matcha Powder Culinary 100g', 'Premium Japanese matcha powder for lattes, baking, and smoothies.', 1499),
        ('Oolong Tea Semi-Oxidized 200g', 'Traditional semi-oxidized oolong with complex flavor and smooth finish.', 1199),
        ('Peppermint Tea 40 Bags', 'Refreshing peppermint tea bags. Great for digestion and after meals.', 449),
        ('White Tea Silver Needle 100g', 'Delicate silver needle white tea with subtle sweetness and light body.', 1899),
        ('Iced Tea Bags Peach 24 Count', 'Peach-flavored iced tea bags. Just steep, chill, and enjoy.', 549),
    ],
    'Grocery': [
        ('Extra Virgin Olive Oil 1L', 'Cold-pressed extra virgin olive oil from Mediterranean olives. Perfect for cooking and dressing.', 899),
        ('Organic Quinoa 500g', 'Premium organic quinoa. High in protein and perfect for healthy meals.', 699),
        ('Raw Forest Honey 500g', 'Pure raw forest honey collected from wildflower meadows. Unprocessed and natural.', 799),
        ('Almond Butter 350g', 'Smooth almond butter made from roasted almonds. No added sugar or oil.', 599),
        ('Basmati Rice 5kg', 'Long-grain aged basmati rice with aromatic fragrance. Ideal for biryani and pulao.', 1299),
        ('Canned Tuna in Olive Oil 6-Pack', 'Premium skipjack tuna in extra virgin olive oil. High protein and omega-3.', 899),
        ('Pasta Sauce Arrabbiata 400g', 'Spicy Italian arrabbiata pasta sauce with San Marzano tomatoes.', 399),
        ('Mixed Nuts Trail Pack 750g', 'Roasted mixed nuts with almonds, cashews, walnuts, and raisins.', 999),
        ('Maple Syrup Pure 250ml', '100% pure maple syrup sourced from Canadian forests. Grade A dark.', 1199),
        ('Coconut Oil Organic 500ml', 'Cold-pressed organic virgin coconut oil. Multi-use for cooking and skincare.', 649),
        ('Dark Chocolate 85% 100g', 'Premium dark chocolate with 85% cocoa content. Rich and intense flavor.', 399),
    ],
}


class Command(BaseCommand):
    help = 'Seed the database with products for all categories'

    def handle(self, *args, **options):
        created_count = 0
        skipped_count = 0

        for category_name, products in PRODUCTS.items():
            category, _ = Category.objects.get_or_create(name=category_name)

            for name, description, price in products:
                _, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'description': description,
                        'price': price,
                        'category': category,
                        'is_approved': True,
                    },
                )
                if created:
                    created_count += 1
                else:
                    skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done! Created {created_count} products, skipped {skipped_count} already existing.'
        ))
