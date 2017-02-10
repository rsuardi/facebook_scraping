import json
import os
import urllib.request


def return_data(url, api_key):
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'Bearer {}'.format(api_key))

    response = urllib.request.urlopen(request)
    encoding = response.headers.get_content_charset()

    data = json.loads(response.read().decode(encoding))

    return data


def get_next_from_data(data):
    if 'paging' in data:
        paging = data['paging']
        if 'next' in paging:
            return paging['next']
        else:
            return None
    else:
        return None


def parse_images(data, user_id, picture_number):
    # Facebook defaults to returning 25 pictures
    for data_object in data:
        picture_url = data_object['source']
        f = open('{}.jpg'.format(picture_number), 'wb')
        f.write(urllib.request.urlopen(picture_url).read())
        f.close()

        # Increment picture number for each picture
        picture_number = picture_number + 1


def record_face_percentages_from_pictures(data, user_id, picture_number):
    face_coordinate_file = open('face_coordinates.txt', 'a')

    # Every data obj has 25 pictures in it
    for data_object in data:
        picture_tags = data_object['tags']['data']
        for data_tag in picture_tags:
            # FIXME: Not working correctly, getting too many tags
            # add in functionality to just get the id tags out
            if 'id' in data_tag:
                if data_tag['id'] == user_id:
                    x_face_coordinate = data_tag['x']
                    y_face_coordinate = data_tag['y']
                    face_coordinate_file.write(
                        "{},{},{}\n".format(picture_number,
                                            x_face_coordinate,
                                            y_face_coordinate))

        picture_number = picture_number + 1
    face_coordinate_file.close()


def main():
    # TODO: create face_coordinate file off the get go/ or something
    base_url = "https://graph.facebook.com/v2.3/"

    # super secret api password thingy!
    facebook_api_key = os.getenv('9d2c58c6bff220bd99f00afc1d045ec6')

    # Make dir for pcitures and change into that directory
    if not os.path.exists("pictures"):
        os.makedirs("pictures")
    os.chdir("pictures")

    # If this script is run multiple times, removes issues with appending coords
    if os.path.isfile('face_coordinates.txt'):
        os.remove('face_coordinates.txt')

    # This is getting out the user id!
    data = return_data(base_url + "me", facebook_api_key)
    # Will need id for parsing photo tags
    user_id = data['id']

    # This is getting out the first set of pictures!
    data = return_data(base_url + "me/photos", facebook_api_key)
    next_ = get_next_from_data(data)

    data = data['data']
    picture_number = 0
    parse_images(data, user_id, picture_number)
    record_face_percentages_from_pictures(data, user_id, picture_number)
    picture_number += len(data)
    print(len(data))

    if next_ is None:
        more_photos = False
    else:
        more_photos = True

    while (more_photos):
        data = return_data(next_, facebook_api_key)
        next_ = get_next_from_data(data)

        data = data['data']
        parse_images(data, user_id, picture_number)
        record_face_percentages_from_pictures(data, user_id, picture_number)

        picture_number += len(data)
        print(len(data))
        if next_ is None:
            more_photos = False

    print("Done!")


if __name__ == '__main__':
    main()