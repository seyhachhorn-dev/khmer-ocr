# Khmer OCR

An experimental **Khmer Optical Character Recognition (OCR)** project focused on recognizing long Khmer text lines while preserving important visual details such as consonants, subscripts, dependent vowels, and diacritics.

The project explores a continuity-first OCR architecture:

```text
Khmer Text-Line Image
        ↓
Resize to Fixed Height
        ↓
Overlapping Horizontal Chunks
        ↓
SE-VGG Feature Extractor
        ↓
Patch / Visual Tokens
        ↓
Transformer Encoder
        ↓
Merge + Global Position
        ↓
BiLSTM Context Smoothing
        ↓
Transformer Decoder
        ↓
Khmer Text
```

## Overview

Khmer OCR presents challenges that are different from simple Latin character recognition.

Khmer text contains visually important structures above and below the main character body. Long text-line images can also have highly variable widths.

Aggressively resizing a long line into a small fixed-size image may destroy these details.

This project therefore follows a simple principle:

> **Preserve local visual detail while recovering global sequence continuity.**

Instead of shrinking an entire text line to a fixed width, the image is resized to a fixed height and divided horizontally into overlapping chunks.

Each chunk is processed locally before the resulting visual sequences are merged and modeled globally.

## Architecture

### 1. Image Preprocessing

Input text-line images are resized to a fixed height of:

```text
48 px
```

The width is calculated proportionally to preserve the original aspect ratio.

For an image with:

```text
height = 80
width  = 1305
```

the scale is:

```text
48 / 80 = 0.6
```

giving:

```text
new height = 48
new width  = 1305 × 0.6 = 783
```

The resulting image is therefore:

```text
48 × 783
```

rather than forcing the image into a fixed width and distorting the text.

### 2. Horizontal Chunking

The resized image is divided into horizontal chunks.

Current configuration:

```text
Chunk size: 48 × 100 px
Overlap:    16 px
Stride:     84 px
```

The stride is calculated as:

```text
stride = chunk_width - overlap
       = 100 - 16
       = 84
```

For example:

```text
Chunk 1:   0 → 100
Chunk 2:  84 → 184
Chunk 3: 168 → 268
Chunk 4: 252 → 352
...
```

Neighboring chunks therefore share 16 pixels.

The overlap helps reduce hard boundary problems when visual structures occur near a crop boundary.

### 3. Padding

The final chunk may contain fewer than 100 pixels.

For example:

```text
Actual final chunk:

┌────────┐
│ Khmer  │
└────────┘
   27px
```

It can be padded to the expected width:

```text
┌─────────────────────────────┐
│ Khmer │                     │
└─────────────────────────────┘
             100px
```

For document images with a white background, white padding is used.

This keeps chunk dimensions consistent:

```text
(48, 100, 3)
```

### 4. SE-VGG Feature Extraction

Each chunk is passed through an SE-VGG-based visual feature extractor.

The CNN learns useful visual patterns such as:

* edges
* curves
* strokes
* character components
* small visual marks
* higher-level shape patterns

The goal at this stage is not to directly predict Khmer characters.

Instead:

```text
Image Pixels
     ↓
SE-VGG
     ↓
Visual Features
```

Squeeze-and-Excitation (SE) blocks are used to refine feature channels while preserving the horizontal reading dimension.

### 5. Visual Tokens

The extracted feature maps are converted into patches.

Each patch becomes a numerical vector representing a small visual region.

```text
Feature Map
    ↓
Patches
    ↓
P1 P2 P3 P4 ... Pn
```

The architecture uses **384-dimensional patch vectors**.

A visual token should not be confused with a visual feature.

```text
Feature
    = detected visual information

Visual Token
    = numerical representation of a visual region
```

A visual token also does not necessarily correspond to one Khmer character.

### 6. Transformer Encoder

The Transformer Encoder models relationships between visual tokens within each chunk.

Conceptually:

```text
P1 ↔ P2 ↔ P3 ↔ P4 ↔ P5
```

A useful mental model is:

```text
CNN
"What visual patterns exist?"

Transformer Encoder
"How are these visual pieces related?"
```

At this stage, context is primarily modeled locally within individual chunks.

### 7. Global Sequence Reconstruction

After local encoding, the encoded chunks are merged into a unified sequence.

```text
Chunk 1 → P1 P2 P3 P4
Chunk 2 → P5 P6 P7 P8
Chunk 3 → P9 P10 P11 P12

              ↓

P1 P2 P3 P4 P5 P6 P7 P8 P9 P10 P11 P12
```

Global positional information is added so the model can understand the ordering of the reconstructed text line.

### 8. BiLSTM Context Smoothing

Although overlapping chunks reduce crop artifacts, each chunk was previously encoded independently.

A bidirectional LSTM processes the merged sequence in both directions:

```text
→ → → → → → →
P1 P2 P3 P4 P5 P6 P7
← ← ← ← ← ← ←
```

This allows sequence positions to receive context from both earlier and later positions.

Its role in this architecture is to improve continuity across the reconstructed line, especially around chunk boundaries.

```text
Merged Visual Sequence
        ↓
BiLSTM
        ↓
Smoothed Context Sequence
```

### 9. Transformer Decoder

The Transformer Decoder converts the encoded visual representation into Khmer text.

Conceptually:

```text
Visual Context
      +
Previously Generated Text
      ↓
Transformer Decoder
      ↓
Next Output Token
```

Generation continues until the output sequence is complete.

```text
Image
  ↓
Visual Representation
  ↓
Sequence Context
  ↓
Transformer Decoder
  ↓
Khmer Text
```

## Project Status

This project is currently under active development and experimentation.

Current progress:

* [x] Understand OCR fundamentals
* [x] Preserve image aspect ratio
* [x] Resize text lines to 48 px height
* [x] Implement horizontal chunking
* [x] Implement 16 px overlap
* [x] Handle final-chunk padding
* [ ] Convert images to PyTorch tensors
* [ ] Implement CNN feature extraction
* [ ] Implement SE blocks
* [ ] Implement patch/token generation
* [ ] Implement Transformer Encoder
* [ ] Implement global sequence merging
* [ ] Implement BiLSTM context smoothing
* [ ] Implement Transformer Decoder
* [ ] Build Khmer OCR dataset pipeline
* [ ] Train model
* [ ] Evaluate Character Error Rate (CER)
* [ ] Add inference API
* [ ] Containerize deployment

## Project Structure

The project structure will evolve as the implementation grows.

```text
khmer-ocr/
├── images/
│   └── khmer.png
├── preprocess.py
├── requirements.txt
├── README.md
└── LICENSE
```

A future structure may look like:

```text
khmer-ocr/
├── configs/
├── data/
├── datasets/
├── models/
│   ├── feature_extractor.py
│   ├── encoder.py
│   ├── sequence_model.py
│   └── decoder.py
├── preprocessing/
│   ├── resize.py
│   └── chunk.py
├── training/
├── evaluation/
├── inference/
├── tests/
├── train.py
├── predict.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Getting Started

### Requirements

* Python 3.10+
* OpenCV
* PyTorch *(required in later stages)*

### Clone

```bash
git clone https://github.com/YOUR_USERNAME/khmer-ocr.git
cd khmer-ocr
```

### Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

For the current preprocessing implementation:

```bash
pip install opencv-python
```

Later, the project will also require PyTorch and supporting machine-learning packages.

## Running Preprocessing

Place a Khmer text-line image at:

```text
images/khmer.png
```

Then run:

```bash
python3 preprocess.py
```

The preprocessing pipeline will:

1. Load the image.
2. Preserve its aspect ratio.
3. Resize it to 48 px height.
4. Divide it into 100 px horizontal chunks.
5. Maintain 16 px overlap between neighboring chunks.
6. Pad short final chunks when necessary.

## Example

Given:

```text
Original shape:
(80, 1305, 3)
```

the image is resized to:

```text
(48, 783, 3)
```

It is then processed as overlapping chunks:

```text
Image width: 783

0         100
├──────────┤
        84         184
        ├──────────┤
                168        268
                ├──────────┤
                         ...
```

Each full model input chunk has the shape:

```text
(48, 100, 3)
```

## Research Direction

The project investigates Khmer OCR as a **long sequence reconstruction problem** rather than simply recognizing isolated character crops.

The main areas of experimentation include:

* preserving Khmer vertical visual information
* overlapping chunk strategies
* CNN/SE-VGG visual feature extraction
* visual token representations
* local Transformer encoding
* global sequence reconstruction
* chunk-boundary continuity
* BiLSTM sequence modeling
* Transformer-based text decoding
* Khmer Unicode-aware preprocessing and evaluation

As development progresses, architectural choices should be validated experimentally rather than assumed to be universally optimal.

## Learning Goals

This repository also serves as a practical learning project for understanding modern OCR systems from the ground up.

The implementation progresses through:

```text
Pixels
  ↓
Image Preprocessing
  ↓
CNN
  ↓
Visual Features
  ↓
Visual Tokens
  ↓
Transformer
  ↓
Sequence Modeling
  ↓
Decoder
  ↓
Khmer Text
```

The goal is to understand not only **how** each component is implemented, but also **what it does, why it exists, and when it is useful**.

## Contributing

Contributions, experiments, bug reports, and discussions related to Khmer OCR are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Add or update tests where appropriate.
5. Open a pull request describing the change and its motivation.

For research-related changes, please include enough information to reproduce the experiment when possible.

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project explores techniques from modern computer vision, sequence modeling, and Transformer-based OCR with a focus on the challenges of Khmer script recognition.

The architecture and implementation are experimental and expected to evolve as training and evaluation results become available.
