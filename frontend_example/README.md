# Instructions

```
git clone git@github.com:galadriel-ai/points-backend.git
cd points-backend
docker run --name add-points -v ./frontend_example:/usr/share/nginx/html:ro -p 80:80 -d nginx
# open http://localhost/add_points.html in browser
```