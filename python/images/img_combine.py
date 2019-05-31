#!/urs/bin/env python3


def image_combine(imgs):
    from PIL import Image

    img_sizes = [Image.open(img).size for img in imgs]

    toImage_w = max([img_size[0] for img_size in img_sizes])
    toImage_h = 0
    for img_size in img_sizes:
        toImage_h += img_size[1]

#    toImage = Image.new('RGBA', (200, 200))
    toImage = Image.new('RGB', (toImage_w, toImage_h))

    print(imgs)
    for i, img in enumerate(imgs):

        subimg = Image.open(img)

        toImage.paste(subimg, (0, i*img_sizes[0][1]))

    return toImage


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--imgs',
                        default=None)

    parser.add_argument('--out_img',
                         default=None, 
                         help='default = "test.png"')

    args = parser.parse_args()

    imgs = eval(args.imgs)
    out_img = args.out_img   

    toImage = image_combine(imgs)
    
    toImage.save(out_img)
