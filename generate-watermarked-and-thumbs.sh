#!/bin/env bash

#use something like this to order them by date taken:
#http://www.linuxjournal.com/content/tech-tip-automaticaly-organize-your-photos-date


# Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec > >(tee logfile.txt)

# Without this, only stdout would be captured - i.e. your
# log file would not contain any error messages.
# SEE answer by Adam Spiers, which keeps STDERR a seperate stream -
# I did not want to steal from him by simply adding his answer to mine.
exec 2>&1

WORKING=./img/working
RAW_FOLDER=./img/raw/all
WATERMARKS_FOLDER=./img/watermarks
WATERMARKED_FOLDER=./img/watermarked
THUMBS_FOLDER=./img/thumbnail


#remove spaces from file names
if [ ! -d "$WORKING" ]; then
    mkdir "$WORKING"
    cp -r $RAW_FOLDER/* $WORKING 
    
    for file in $WORKING/*; do
        mv --backup=numbered -- "$file" "${file// /_}"
    done
fi

for file in $WORKING/*
do
    
    # next line checks the mime-type of the file
    IMAGE_TYPE=`file --mime-type -b "$file" | awk -F'/' '{print $1}'`
    
    if [ x$IMAGE_TYPE = "ximage" ]; then
        IMAGE_SIZE=`identify -format "%wx%h" $file`
        #`file -b $file | sed 's/ //g' | sed 's/,/ /g' | awk  '{print $2}'`
        WIDTH=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $1}'`
        HEIGHT=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $2}'`          
        filename=$(basename "$file")
        extension="${filename##*.}"
        filename="${filename%.*}"
        
        WATERMARK_IMG="${WATERMARKS_FOLDER}/${filename}-watermark.png"
        if [[ ! -f "$WATERMARK_IMG" ]]; then
            echo "generating watermark for $file"
            echo "  image type: $IMAGE_TYPE"
            echo "  size: $IMAGE_SIZE, width: $WIDTH, height: $HEIGHT"
            #create trans img w watermark with custom size
            
            #first way is to use image scale, but bash does integer rounding
            #S_W=4
            #S_H=20
            #W=$((WIDTH - $((WIDTH/S_W))))
            #H=$((HEIGHT - $((HEIGHT/S_H))))

            #more simple to just move down from top left corner, the safe, but ugly, approach
            D_W=180
            D_H=30
            W=$((WIDTH - D_W))
            H=$((HEIGHT - D_H))
            echo "  mark location: $W, $H"
            convert -size "$WIDTH"x"$HEIGHT" xc:transparent -font Overpass-bold -pointsize 28 -fill PapayaWhip -draw "text $W,$H 'octavian g'" "$WATERMARK_IMG"
            
            echo "  watermark: $WATERMARK_IMG"
            
            
            composite -dissolve 70% -quality 100 "$WATERMARK_IMG" "$file" "${WATERMARKED_FOLDER}/${filename}_marked.${extension}"  
            echo "  watermarked image output: ${WATERMARKED_FOLDER}/${filename}_marked.${extension}"
        else
            echo "  file $WATERMARK_IMG already exists, skipping"
        fi
    fi 
done

echo "" > images.json

for file in $WATERMARKED_FOLDER/*
do
    
    # next line checks the mime-type of the file
    IMAGE_TYPE=`file --mime-type -b "$file" | awk -F'/' '{print $1}'`
    
    if [ x$IMAGE_TYPE = "ximage" ]; then
        IMAGE_SIZE=`identify -format "%wx%h" $file`
        #`file -b $file | sed 's/ //g' | sed 's/,/ /g' | awk  '{print $2}'`
        WIDTH=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $1}'`
        HEIGHT=`echo $IMAGE_SIZE | sed 's/x/ /g' | awk '{print $2}'`  
        
        # If the image width is greater that 200 or the height is greater that 150 a thumb is created
        #if [ $WIDTH -ge  201 ] || [ $HEIGHT -ge 151 ]; then
        #This line convert the image in a 200 x 150 thumb 
        filename=$(basename "$file")
        extension="${filename##*.}"
        filename="${filename%.*}"
        THUMB_IMG="${THUMBS_FOLDER}/${filename}_thumb.${extension}"
        if [[ ! -f $THUMB_IMG ]]; then
            echo "generating thumb for $file"
            echo "image type: $IMAGE_TYPE"
            echo "size: $IMAGE_SIZE, width: $WIDTH, height: $HEIGHT"
            #generate thumbnail:
            convert -sample 200x150 "$file" "$THUMB_IMG" 
            
        else
            echo "  file $THUMB_IMG already exists, skipping"
        fi
        
        echo "{
          \"url_wt\":\"${THUMBS_FOLDER}/${filename}_thumb.${extension}\",
          \"url_w\":\"${WATERMARKED_FOLDER}/${filename}.${extension}\",
          \"title\":\"title\"
}," >> images.json
        
        #fi
    fi     
done
