import http.client
import json
import time
import sys
import collections




def request(BASE_URL, key, end_point):
    conn = http.client.HTTPSConnection(BASE_URL)
    url = end_point.format(key)
    conn.request("GET", url)
    response = conn.getresponse().read()
    return json.loads(response)


def get_movie_list(key):
    BASE_URL = r"api.themoviedb.org"
    end_point = r"/3/discover/movie?api_key={}&language=en-US&sort_by=popularity.desc&with_genres=18&primary_release_date.gte=2003-12-31&page={}"
    movie_list = []
    for i in range(1,21):
        ep = end_point.format(key, str(i))
        r = request(BASE_URL, key, ep)
        results = r['results']
        for result in results:
            movie_list.append([result['id'], result['title']])
    return movie_list[:349]


def get_similar_movie(movie_list, key):
    BASE_URL = r"api.themoviedb.org"
    end_point = r"/3/movie/{}/similar?api_key={}&language=en-US&page=1"
    new_list = []
    movie_set = []
    start = time.time()
    i = 1
    for movie in movie_list:
        if i%40 == 0:
            if time.time()-start < 10:
                sleep_time =10-time.time()-start
                print("sleep for {}\n".format(str(sleep_time)))
                time.sleep(sleep_time)
            start = time.time()
        movie_id = movie[0]
        print("Getting similar movies for {}\n".format(movie[1]))
        ep = end_point.format(movie_id, key)
        r = request(BASE_URL, key, ep)
        results = r['results']
        for result in results[:5]:
            similar_movie_id = result['id']
            similar = [movie_id, similar_movie_id]
            if tuple(sorted(similar)) in movie_set:
                pass
            else:
                new_list.append(similar)
                movie_set.append(sorted(similar))
    return new_list
                

def write_data(output_file_name, data_list):
    output = open(output_file_name, 'a')
    for l in data_list[:-1]:
        output.write(str(l[0]))
        output.write(',')
        output.write(str(l[1]))
        output.write('\n')
    l = data_list[-1]
    output.write(str(l[0]))
    output.write(',')
    output.write(str(l[1]))
    output.close()

if __name__ == "__main__":
    key = str(sys.argv[1])
    print("Getting movie list\n")
    movie_list =get_movie_list(key)
    similar_movies = get_similar_movie(movie_list, key)
    print("Writing data\n")
    write_data("movie_ID_name.csv", movie_list)
    write_data("movie_ID_sim_movie_ID.csv", similar_movies)
    
    
    