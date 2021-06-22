def findRoutes(controllerFileName, tag="HttpGet"):
    with open(controllerFileName, "r") as controllerFile:
        text = controllerFile.read()
    routePrefix = "/" + getRoutePrefix(text)
    routes = []
    tagStart = text.find(tag)
    while tagStart >= 0:
        routeStart = text.find("[Route", tagStart+1)
        if routeStart >= 0:
            routeEnd = text.find("]", routeStart+1)
            route = getDoubleQuotedText(text[routeStart:routeEnd+1])
            routes.append(f"      {routePrefix}/{route}")
        tagStart = text.find(tag, routeStart+1)
    return routes

def getRoutePrefix(text):
    start = text.find("[RoutePrefix")
    end = text.find("]", start+1)
    return getDoubleQuotedText(text[start:end+1])

def getDoubleQuotedText(text):
    start = text.find('"')
    end = text.find('"', start+1)
    return text[start+1:end]

import os, sys
if __name__ == "__main__":
    for controllerFileName in sys.argv[1:]:
        print(f"\x1b[31m\x1b[1m{os.path.basename(controllerFileName)}\x1b[0m")
        for tag in 'HttpGet', 'HttpPut', 'HttpPost', 'HttpDelete':
            routes = findRoutes(controllerFileName, tag=tag)
            if len(routes) > 0:
                print(f"\x1b[32m    {tag}\x1b[0m")
                for route in routes:
                    print(route)

