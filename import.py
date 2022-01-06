import db
import dict_lookup
import re
import format
from pathlib import Path
from datetime import datetime

def import_vocab():
    df = db.import_vocab(num_days_history_or_last='last')

    df['front'] = df.apply(lambda x: format.highlight_lookup_word(
        x.usage, x.word, x.stem
    ), axis=1)
    df['reverse'] = df['word'].apply(dict_lookup.lookup_and_filter)
    df['tags'] = '日本語 kindle'

    df_out = df[['front','reverse','tags']]

    output_folder = Path("output/")
    output_file = output_folder / f"kindle_vocab_export_{datetime.now():%Y%m%d_%H%M}.csv"

    df_out.to_csv(
        output_file,
        header=False,
        index=False,
        )
    db.save_last_run_time_str()
    print('all done 🖖')

if __name__ == "__main__":
    import_vocab()