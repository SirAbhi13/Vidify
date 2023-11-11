# VIDIFY

- This is a Django video processing app that uses the `FFMPEG` library at the backend to extract audio and watermark to the uploaded video.

- The application also implements custom watermark overlay feature where the user can either supply exact `x,y` coordinates or use predefined places to put watermark on.

- The application also stores the details of the Videos and the Processed videos in the PostgreSQL db.

- The app follows a modular structure, with clear and concise code.
- The application uses the `APIView` class from the django-rest-framework to have a better control over the backend api endpoints and responses.
- Makefile introduced for efficient local setup and development.


# Features

1. **Audio Extraction:**
   - Upload a video file.
   - Extract the audio from the video.
   - Download the extracted audio file in mp3 format.

2. **Video Watermarking:**
   - Upload a video and a watermark image.
   - Overlay the watermark on the video at a customizable position.
        - User can provide exact `x,y` coordinates (starting from top left of the video)
        - User can use predefined positions supported by API which are:
            - `top-left`
            - `top-right`
            - `bottom-right`
            - `bottom-left`
            - `center`
   - Store information about the processed video and watermarking parameters along with the path of files and time of edit.
   - Download the video with watermark!


3. **Containerized Application:**
   - Dockerized for easy deployment and scalability.
   - The DB persistence is maintained through docker volumes where docker attaches a local volume to the DB service so as to have backup data in case the container is closed say through `docker compose down`.
   - Backend data (stored videos and audio files and images) are also persisted.
   - Instructions for containerizing the application included in the README.

# Local setup:

1. **Running Directly From Repository**

    ### Please ensure you have FFMPEG library installed
    1) Clone the repository and cd into it.

    2) run the command `make setup` to install dependencies and create .env file from .env.example.

    3) Start the virtual environment by using the command `source src/.venv/bin/activate`.

    3) open .env file and add the appropriate values below `# FOR DJANGO APP` comment for the database settings (there are some place holder settings for docker use, replace them)

    5) Now to run the backend server, simply type `make runserver` to initiate the server at http://127.0.0.1:8000/

2. **Using Docker Compose**
    1) Clone the repository and cd into it.

    2) Run the command `cp .env.example .env` to generate a *.env* file. Change the values if you wish to, although I have already populated the fields with Test values.

    3) Now we can start creating images and running up the containers. Use the commands in root directory itself.

    4) Write these commands to start using the app:

        ```
        sudo docker compose build
        ```
        -   `docker-compose build` builds the images for the listed services in the `docker-compose.yml` file, here they will be backend and db.

        ```
        docker compose up
        ```
        - `docker compose up` creates the respective containers from the images of the services and composes them together also creating a local network for them in order for the services to communicate.

        - A backend server would have started at http://127.0.0.1:8000/.

    5) To stop the containers:
        ```
        docker compose down
        ```
        - `docker compose down` command will stop running containers, but it also removes the stopped containers as well as any networks that were created.

# How to use the App
#### ACCEPTED IMAGE FORMATS : ["jpg", "png", "svg", "eps"]
#### ACCEPTED VIDEO FORMATS : ["mp4", "avi", "mkv", "mov", "wmv"]


1) Go to http://127.0.0.1:8000/accounts/api/signup/ and register a user
    - You need to send `username` and `password` fields.
    - Request should be `POST`

2) Go to http://127.0.0.1:8000/accounts/api/login/ and login with credentials of a signed up user
    - You need to send `username` and `password` fields.
    - Request should be `POST`
    - Copy the token value from `access` field in the body of the response

3) #### Extract Audio from an uploaded Video
    - Go to http://127.0.0.1:8000/video/api/extract-audio/
    - Add the `Authorization` Header key to the request. The value will be `Bearer {token}`
        ```
        Example
        Authorization : Bearer {pasted token copied above, without braces}
        ```
    - In the body, send `video_file` field with a video.
    - You will get a response with the mp3 file which can be downloaded.
4) #### Overlay a watermark on an video
    - Go to http://127.0.0.1:8000/video/api/watermark-video/
    - Add the `Authorization` Header key to the request. The value will be `Bearer {token}`
        ```
        Example
        Authorization : Bearer {pasted token copied above, without braces}
        ```
    - In the body, send `video_file` field with a video, send `image_file` field with a an image/logo.

    - [OPTIONAL] SEND `scale` field to scale the watermark respective to height of video.
        - Default value is `0.2`
        - Value should be less than `1` and should have at most 3 decimals

    - If you wish to use custom coordinates for the position of the watermark
        - Send `custom_coordinate_X` field with the X position AND
        - Send `custom_coordinate_Y` field with the Y position
        - Both fields are important for this to work
        - (0,0) is the top-left pixel in the video.
        - Coordinates should be under the value of the resolution of the video.

    - ### OR
    - You can also use the predefined positions in the API
    - Send `lazy_position` field with any of the following values:
            - `top-left`
            - `top-right`
            - `bottom-right`
            - `bottom-left`
            - `center`
    - If both coordinates and lazy_position is supplied, then the coordinates are given priority.
    - Download the video with the watermark
