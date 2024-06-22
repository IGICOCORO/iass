import json
from django.http import HttpResponse
import subprocess
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request, chemin=""):
    method = request.method
    data = json.dumps(json.loads(request.body.decode()))
    commande = ["sudo", "curl", "-X", method, "--unix-socket", "/tmp/firecracker.socket", "--data", data, f"http://localhost/{chemin}"]
    reponse = subprocess.check_output(commande)
    if "fault_message" in reponse.decode():
        return HttpResponse(reponse, status=400)
    return HttpResponse(reponse)