from pipeline import Pipeline
pipe = Pipeline('videotestsrc pattern=black ! autovideosink', '../props.json')
pipe.play()
