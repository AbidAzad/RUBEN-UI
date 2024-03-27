import qrcode

def generate_google_maps_link(start_location, end_location):
    base_url = "https://www.google.com/maps/dir/"
    walking_mode = "/data=!4m2!4m1!3e2"
    link = f"{base_url}{start_location}/{end_location}{walking_mode}"
    return link

def generate_qr_code(link, output_file="qr_code.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)

if __name__ == "__main__":
    start_location = "Rutgers+University+Busch+Student+Center"
    end_location = "Richard+Weeks+Hall+of+Engineering"

    google_maps_link = generate_google_maps_link(start_location, end_location)
    generate_qr_code(google_maps_link)
