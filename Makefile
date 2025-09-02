TCG_HOME = $(subst \,/,$(APPDATA))/godot/app_userdata/Turing\ Complete
SCHEMATICS_DIR = $(TCG_HOME)/schematics
CIRCUITS = architecture/Eater/circuit.json \
	component_factory/DecimalDecoder/circuit.json \
	component_factory/FullSevenSegmentDecoder/circuit.json \
	component_factory/RegisterPassPlus/circuit.json \
	component_factory/SevenSegmentDecoderRom/circuit.json

TRANSCRIBE=../tcg-transcribe/main.py

all: $(CIRCUITS)

# Checking against the game files is hairball so just make with -B
%.json:
	mkdir -p $(@D)
	find $(SCHEMATICS_DIR)/$(*D) -iname *.rom -exec cp {} $(@D) \;
	find $(SCHEMATICS_DIR)/$(*D) -iname sandbox -exec cp -r {} $(@D) \;
	$(TRANSCRIBE) $(SCHEMATICS_DIR)/$*.data > $@