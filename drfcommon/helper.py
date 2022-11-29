

def handler_err(errors, msg="请检查请求参数") -> str:
    if isinstance(errors, dict):
        for key, value in errors.items():
            if isinstance(value, list):
                value = value[0]
            msg = str(value)
            return msg
    if isinstance(errors, list):
        for v in errors:
            return v
    return msg


def demo_dict():
    errors = {
        "items": [
            "问卷内容不能为空"
        ]
    }
    msg = handler_err(errors)
    print(msg)


def demo_list():
    errors = [
        "问卷内容不能为空"
    ]
    msg = handler_err(errors)
    print(msg)


if __name__ == '__main__':
    demo_dict()
    demo_list()