import cv2


class Logger:
    @staticmethod
    def show_img(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def show_rectangles(rectangles, img, text=False):
        for x, y, w, h in rectangles:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            if text:
                cv2.putText(img, '{0},{0}'.format(x, y), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        Logger.show_img(img)

    @staticmethod
    def show_circles(positions, img, text=False):
        for position in positions:
            x, y = position
            cv2.circle(img, position, 2, (0, 255, 255), 2)
            if text:
                cv2.putText(img, '{0},{0}'.format(x, y), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        Logger.show_img(img)
