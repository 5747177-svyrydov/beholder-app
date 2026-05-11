import * as R from 'ramda';
import { div, span } from '@cycle/dom';

export function renderMarkerPairNode(props, { panX, panY }) {
  const { x, y, uuid, selected, inputs, outputs } = props;

  return div(
    `#${uuid}.draggable-node.marker-pair-node`,
    { style: { transform: `translate(${x + panX}px, ${y + panY}px)` }, class: { selected }, dataset: { uuid } },
    [
      div('.node-inputs', R.toPairs(inputs).map(
        ([key, { offsetX, offsetY, source, valueType }]) =>
          span('.input-point', { class: { connected: !R.isNil(source) }, dataset: { type: 'input', valueType, name: key, parent: uuid, offsetX, offsetY } }, key)
      )),
      span('.marker-pair-node-text', 'Marker Pair'),
      div('.node-outputs.center-outputs', R.toPairs(outputs).map(
        ([key, { offsetX, offsetY, valueType }]) =>
          span('.output-point', { dataset: { type: 'output', name: key, parent: uuid, offsetX, offsetY, valueType } }, [key, span('.marker-data', '0')])
      ))
    ]
  );
};

export function createMarkerPairNode(props, uuid) {
  return {
    ...props,
    uuid,
    outputs: {
      DIST: { name: 'DIST', offsetX: 270, offsetY: 39, targets: [], valueType: 'number' },
      ANG: { name: 'ANG', offsetX: 270, offsetY: 59, targets: [], valueType: 'number' },
      POS_X: { name: 'POS_X', offsetX: 270, offsetY: 79, targets: [], valueType: 'number' },
      POS_Y: { name: 'POS_Y', offsetX: 270, offsetY: 99, targets: [], valueType: 'number' }
    },
    inputs: {
      ID_A: { offsetX: 0, offsetY: 39, source: null, sourceField: null, valueType: 'number' },
      ID_B: { offsetX: 0, offsetY: 79, source: null, sourceField: null, valueType: 'number' },
      SOURCE: { offsetX: 0, offsetY: 119, source: null, sourceField: null, valueType: 'feed' }
    },
    selected: false,
  };
}