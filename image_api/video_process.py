from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from moviepy.editor import VideoFileClip
from django.http import StreamingHttpResponse
import tempfile

class VideoUploadView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, format=None):
        video_file = request.data['file']
        start_time=request.date['start_time']
        end_time=request.date['end_time']

        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            temp_video.flush()

            # Load the video with moviepy
            video = VideoFileClip(temp_video.name)

            # Perform your custom function (e.g., extracting a clip)
            #start_time = 10  # Start at 10 seconds
            #end_time = 20    # End at 20 seconds
            clip = video.subclip(start_time, end_time)

            # Save the result to another temporary file
            with tempfile.NamedTemporaryFile(delete=True, suffix='.mp4') as temp_output:
                clip.write_videofile(temp_output.name, codec='libx264')

                # Stream the output video back to the client
                def stream_video():
                    with open(temp_output.name, 'rb') as f:
                        yield from f

                response = StreamingHttpResponse(stream_video(), content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="output_clip.mp4"'
                return response
