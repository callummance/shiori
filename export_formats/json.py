import json
import base64
import logging

def export(args, opts, library):
    dicts = list(map(lambda song: export_song(args, song), library.library))
    json_str = json.dumps(dicts)
    if "file" in opts:
        with open(opts["file"], "w") as tg:
            tg.write(json_str)
    else:
        print(json_str)


def export_song(args, song):
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
    if args.covers:
        try:
            d["cover"] = base64.b64encode(song.load_cover()).decode("utf-8")
        except AttributeError:
            logging.info("Song " + song.title + " is does not have cover included.")
        except Exception as e:
            logging.warning("failed to load cover for " + song.title + " with error " + str(e))
    if args.bgs:
        try:
            d["bg"] = base64.b64encode(song.load_bg()).decode("utf-8")
        except AttributeError:
            logging.info("Song " + song.title + " is does not have background included.")
        except Exception as e:
            logging.warning("failed to load background for " + song.title + " with error " + str(e))
    return d
