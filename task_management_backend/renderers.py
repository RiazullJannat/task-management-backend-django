from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context and 'response' in renderer_context:
            status_code = renderer_context['response'].status_code
            
            # Prevent double wrapping if data is already formatted correctly
            if isinstance(data, dict) and 'success' in data and 'message' in data:
                return super().render(data, accepted_media_type, renderer_context)

            if status_code >= 400:
                msg = 'An error occurred'
                errs = data
                if isinstance(data, dict):
                    msg = data.get('message', data.get('detail', 'An error occurred'))
                    errs = data.get('errors', data)

                response_data = {
                    'success': False,
                    'message': msg,
                    'errors': errs,
                    'data': None
                }
            else:
                msg = 'Success'
                payload = data
                if isinstance(data, dict) and ('message' in data or 'data' in data):
                    msg = data.get('message', 'Success')
                    payload = data.get('data', data)

                response_data = {
                    'success': True,
                    'message': msg,
                    'data': payload
                }
            return super().render(response_data, accepted_media_type, renderer_context)
            
        return super().render(data, accepted_media_type, renderer_context)
