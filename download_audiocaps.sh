#!/bin/bash
export PATH=$PATH:$(pwd)

SAMPLE_RATE=16000

save_dir=corpora/audiocaps_data
mkdir -p "${save_dir}"
mkdir -p "${save_dir}/train"

# fetch_clip(videoID, startTime, endTime)
fetch_clip() {
  outname="${save_dir}/train/$1"
  if [ -f "${outname}.wav" ]; then
    echo "Already have $1.wav"
    return
  fi
  stime=$2
  etime=$(($2+10))
  echo "Fetching $1 from $stime to $etime seconds..."

  youtube-dl https://youtube.com/watch?v=$1 \
    --quiet --extract-audio --audio-format wav \
    --output "$outname.%(ext)s"
  if [ $? -eq 0 ]; then
    # If we don't pipe `yes`, ffmpeg seems to steal a
    # character from stdin. I have no idea why.
    yes | ffmpeg -loglevel quiet -i "$outname.wav" -ar $SAMPLE_RATE \
      -ac 1 -ss "$stime" -to "$etime" "${outname}_out.wav"
    mv "${outname}_out.wav" "$outname.wav"
  else
    # Give the user a chance to Ctrl+C.
    sleep 1
  fi
}

grep -E '^[^#]' | while read line
do
  fetch_clip $(echo "$line" | sed -E 's/, / /g')
done
