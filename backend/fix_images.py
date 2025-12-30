import sqlite3

DATABASE = 'food_delivery.db'

def fix_broken_images():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Fix Bacon Burger image
    c.execute('''UPDATE menu_items 
                 SET image_url = ? 
                 WHERE name = ?''', 
              ('https://images.unsplash.com/photo-1553979459-d2229ba7433a?w=400&h=300&fit=crop&q=80', 'Bacon Burger'))
    
    # Fix Tuna Roll image
    c.execute('''UPDATE menu_items 
                 SET image_url = ? 
                 WHERE name = ?''', 
              ('https://images.unsplash.com/photo-1611143669185-af800c5eabef?w=400&h=300&fit=crop&q=80', 'Tuna Roll'))
    
    conn.commit()
    conn.close()
    print("✅ Fixed broken images for Bacon Burger and Tuna Roll!")

if __name__ == '__main__':
    fix_broken_images()

