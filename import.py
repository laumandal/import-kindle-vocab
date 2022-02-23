import db
import dict_lookup
import format
from pathlib import Path
from datetime import datetime
import fire


def import_vocab(
    highlight_study_word=True,
    tags="日本語 kindle",
    csv_encoding="utf-8-sig",
    num_days_history=None,
):
    """Run the import vocab process and save as a CSV."""
    # import vocab from kindle db
    df = db.import_vocab(num_days_history=num_days_history)

    if len(df)>0:
        if highlight_study_word is True:
            df["front"] = df.apply(
                lambda x: format.highlight_lookup_word(x.usage, x.word, x.stem), axis=1
            )

        # get definitions from the OSX dictionary for reverse of the cards
        df["reverse"] = df["word"].apply(dict_lookup.lookup_and_filter)
        df["tags"] = df["title"].apply(format.format_title_for_tags) + " " + tags

        # save file out as CSV
        df_out = df[["word", "front", "reverse", "tags", "lookup_timestamp"]]

        output_folder = Path(__file__).resolve().parent / "output/" # first part is just current folder
        output_file = (
            output_folder / f"kindle_vocab_export_{datetime.now():%Y%m%d_%H%M}.csv"
        )
        df_out.to_csv(output_file, header=False, index=False, encoding=csv_encoding)
        db.save_last_run_time_str()
        print("all done 🖖")
    elif len(df) ==0:
        print("No new vocab to import 🤷‍♂️")


if __name__ == "__main__":
    fire.Fire()
