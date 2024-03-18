import pyeraser
import sys

def main():
    if len(sys.argv) != 5 and len(sys.argv) != 6:
        print('Usage: python pyeraser.py <current_word(s)> <new_word> <quantity_of_products> <wait_time>')
        sys.exit(1)
        
    current_words = sys.argv[1].split(',')
    new_word = sys.argv[2]
    quantity_products = int(sys.argv[3])
    wait_time = float(sys.argv[4])
    last_produtc_id = None
    if len(sys.argv) == 6:
        last_produtc_id = sys.argv[5]

    eraser = pyeraser.Eraser(current_words, new_word, quantity_products, wait_time, last_produtc_id)
    eraser.run()
    
    
if __name__ == '__main__':
    main()