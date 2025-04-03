from django.http import JsonResponse
from .chroma_utils import ChromaDBManager
from django.views.decorators.csrf import csrf_exempt

chroma_manager = ChromaDBManager()

@csrf_exempt
def consulta(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse(
            {"error": "La consulta 'q' es requerida"},
            status=400
        )
    
    try:
        results = chroma_manager.query_documents(query)
        
        simplified_results = [{"content": result["content"]} for result in results]
        
        return JsonResponse({"query": query, "results": simplified_results})
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )