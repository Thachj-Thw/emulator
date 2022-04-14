import cv2
import numpy as np


def get_pos_img(
    obj: str,
    _in: bytes,
    center: bool = True,
    multi: bool = False,
    threshold: float = 0.8,
    eps: float = 0.05,
    show: bool = False
) -> list:
    try:
        img_base = cv2.imdecode(np.frombuffer(_in, dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        tem = cv2.imread(obj)
        height, width = tem.shape[:2]
        result = cv2.matchTemplate(img_base, tem, cv2.TM_CCOEFF_NORMED)
        pos = []
        if multi:
            y_loc, x_loc = np.where(result >= threshold)
            rectangles = []
            for x, y in zip(x_loc, y_loc):
                rectangles.append([int(x), int(y), int(width), int(height)])
                rectangles.append([int(x), int(y), int(width), int(height)])
            for x, y, w, h in cv2.groupRectangles(rectangles, 1, eps)[0]:
                if show:
                    cv2.rectangle(img_base, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if center:
                    pos.append((x + w // 2, y + h // 2))
                else:
                    pos.append((x, y))
        else:
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val > threshold:
                if show:
                    cv2.rectangle(img_base, max_loc, (max_loc[0] + width, max_loc[1] + height), (0, 0, 255), 2)
                if center:
                    pos.append((max_loc[0] + width // 2, max_loc[1] + height // 2))
                else:
                    pos.append(max_loc)
        if show:
            cv2.imshow("show", img_base)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return pos
    except Exception as e:
        print(e)
        return []
