#!/usr/bin/pythonwin

from PIL import ImageFile, ImageStat
import urllib, sys

def lowerBound(rms, stddev):
  return int(max(0, rms - stddev))

def upperBound(rms, stddev):
  return int(min(255, rms + stddev))

def calculateBoundaries(im):
  """Calculates the upper and lower boundaries
  of levels to take into consideration for
  picking out the maximum.
  """
  stats = ImageStat.Stat(im)

  lb = map(lowerBound, stats.rms, stats.stddev)
  ub = map(upperBound, stats.rms, stats.stddev)

  return (lb, ub)

def splitHistogram(histogram):
  return [ histogram[x:x+256]  for x in (0, 256, 512) ]

def maxCount(histogram, lb, ub):
  return max(histogram[lb:ub])

def getLevel(histogram, lb, ub, pcount):
  return histogram[lb:ub].index(pcount) + lb

def getPeaks(im, lb, ub):
  """Returns the level of maximum pixel count
  withing lb and ub for each color channel.
  Assumes RGB
  """
  # Get the histogram for the image
  h = splitHistogram( im.histogram() )
  # Get the max pixel count for each channel between lb and ub
  counts = map(maxCount, h, lb, ub)
  # Get the level of max pixel count for each channel between lb and ub
  levels = map(getLevel, h, lb, ub, counts)

  return tuple(levels)

def clipHighlights(levels, highlight=255):
  levels = list(levels)
  max_level = float( max(levels) )
  if max_level > highlight:
    for i in range(len(levels)):
      levels[i] = int(levels[i] * (highlight / max_level))

  return tuple(levels)

def getImageFromURL(url):
  fp = urllib.urlopen(url)
  p = ImageFile.Parser()

  while 1:
    s = fp.read(1024)
    if not s:
      break
    p.feed(s)

  im = p.close()

  return im

def getImageFromFile(fn):
  fp = open(fn, 'rb')
  p = ImageFile.Parser()

  while 1:
    s = fp.read(1024)
    if not s:
      break
    p.feed(s)

  im = p.close()

  return im  

def average(im, xy):
  channels = [0] * len(im.getbands())
  for delta_x in (-2, -1, 0, 1, 1):
    for delta_y in (-2, 1, 0, 1, 1):
      p = im.getpixel((xy[0] + delta_x, xy[1] + delta_y))
      channels = [channels[i] + p[i] for i in range(len(p))]
  return [val / 25.0 for val in channels]

def saturation(rgb):
  r,g,b = rgb
  rf = float(r)
  gf = float(g)
  bf = float(b)
  rf = rf/255.0
  gf = gf/255.0
  bf = bf/255.0
  inten = (rf+gf+bf)/3.0
  if(not((r==b) and (r==g))):
    min = rf
    if(min>gf): min = gf
    if(min>bf): min = bf
    sat=1.0-(min/inten)
  else:
    sat=-1.0
  return sat

def getSampleLocations(im):
  width, height = im.size
  positions = []
  for delta_x in range(1,5):
    for delta_y in range(1,5):
      positions.append((delta_x * width / 5, delta_y * height / 5))
  return positions

def mostSaturatedDarkSample(im, level=255):
  max_sat = -1
  for xy in getSampleLocations(im):
    test_pixel = average(im, xy)
    sat = saturation(test_pixel)
    avg = max(.5, (sum(test_pixel)/len(test_pixel))/float(level))
    weighted_sat = sat / (avg * avg * avg)
    if(weighted_sat > max_sat):
      max_sat = weighted_sat
      pixel = map(int, test_pixel)
  return list(pixel)

def mostSaturatedDarkSample_highlight_clip(fn=None, url=None, level=255):
  if fn:
    im = getImageFromFile(fn)
  else:
    im = getImageFromURL(url)
  levels = mostSaturatedDarkSample(im, level)
  return clipHighlights(levels, level)
  

def rms_highlight_clip(fn=None, url=None, level=255):
  if fn:
    im = getImageFromFile(fn)
  else:
    im = getImageFromURL(url)
  lb, ub = calculateBoundaries(im)
  peaks = getPeaks(im, lb, ub)
  return clipHighlights(peaks, level)



if __name__ == '__main__':
  """Currently this handles only RGB.
  For more advanced multi-mode handling,
  getPeaks() should be modified.
  """

  # Set the max level for an individual channel (0-255)
  MAX_LEVEL = 110
  
  # Open the image
  im = getImageFromURL(sys.argv[1])
  # Calculate the upper and lower bounds for each channel
  lb, ub = calculateBoundaries(im)
  print 'lb, ub:', lb, ub
  peaks = getPeaks(im, lb, ub)
  print 'peaks: ', peaks
  levels = clipHighlights(peaks, MAX_LEVEL)
  print 'levels: ', levels
  print [hex(x) for x in levels]
