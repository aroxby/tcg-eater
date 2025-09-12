TCG_HOME = $(subst \,/,$(APPDATA))/godot/app_userdata/Turing\ Complete
IMP_SCHEMATICS_DIR = $(TCG_HOME)/schematics
EXP_SCHEMATICS_DIR = schematics
IMP_CIRCUITS = architecture/Eater/circuit.json \
	component_factory/DecimalDecoder/circuit.json \
	component_factory/FullSevenSegmentDecoder/circuit.json \
	component_factory/SevenSegmentDecoderRom/circuit.json
EXP_CIRCUITS = $(addprefix $(EXP_SCHEMATICS_DIR)/,$(subst .json,.data,$(IMP_CIRCUITS)))
TRANSCRIBE=../tcg-transcribe/main.py

.PHONY: always
always:

.PHONY: import
import: $(IMP_CIRCUITS)

.PHONY: export
export: $(EXP_CIRCUITS)

$(EXP_SCHEMATICS_DIR)/%.data:
	mkdir -p $(@D)
	find $(*D) -iname *.rom -exec cp {} $(@D) \;
	find $(*D) -iname sandbox -exec cp -r {} $(@D) \;
	$(TRANSCRIBE) $(*).json $(@)

# Checking against the game files is hairball so we just force it
%.json: always
	mkdir -p $(@D)
	find $(IMP_SCHEMATICS_DIR)/$(*D) -iname *.rom -exec cp {} $(@D) \;
	find $(IMP_SCHEMATICS_DIR)/$(*D) -iname sandbox -exec cp -r {} $(@D) \;
	$(TRANSCRIBE) $(IMP_SCHEMATICS_DIR)/$*.data $@
