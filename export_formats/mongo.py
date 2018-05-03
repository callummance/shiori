import pymongo
import logging

def export(args, opts, library):
    if not ("mongo_uri" in opts and "mongo_db" in opts):
        logging.error("Export to mongo databse requires more data.")
        logging.error("Please include `--export-opts \"mongo_uri=mongodb://<addr>:<port>,mongo_db=<db_name>,mongo_collection=<collection_name>\"`")
        return
    else:
        client = pymongo.MongoClient(opts["mongo_uri"])
        collection = client[opts["mongo_db"]][opts["mongo_collection"]]
        for song in library.library:
            export_song(args, collection, opts, song)

def export_song(args, c, opts, song):
    if "keep_existing_data" in opts and opts["keep_existing_data"].lower() == "true":
        #Should just write new entries
        id = c.insert_one(create_song_dict(args, song))
    else:
        #Check if there is an existing match based on title, artist, duet, language and creator
        filter_dict = {
            "title": song.title,
            "artist": song.artist,
            "is_duet": song.is_duet,
        }
        try:
            filter_dict["language"] = song.language
        except:
            pass
        try:
            filter_dict["creator"] = song.creator
        except:
            pass
        res = c.find_one_and_replace(filter_dict, create_song_dict(args, song), upsert=True)


def create_song_dict(args, song):
    d = dict(song.__dict__)
    if not args.pb_specific:
        d.pop("textfile", None)
        d.pop("filename", None)
        d.pop("startdelay", None)
        d.pop("edition", None)
        d.pop("cover_path", None)
        d.pop("video_path", None)
        d.pop("background_path", None)
        d.pop("mp3file", None)
        d.pop("dir", None)
    if args.covers:
        try:
            d["cover"] = song.load_cover()
        except AttributeError:
            logging.info("Song " + song.title + " is does not have cover included.")
        except Exception as e:
            logging.warning("failed to load cover for " + song.title + " with error " + str(e))
    if args.bgs:
        try:
            d["bg"] = song.load_bg()
        except AttributeError:
            logging.info("Song " + song.title + " is does not have background included.")
        except Exception as e:
            logging.warning("failed to load background for " + song.title + " with error " + str(e))
    return d
