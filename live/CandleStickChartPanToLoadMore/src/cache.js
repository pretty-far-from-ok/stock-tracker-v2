					<MovingAverageTooltip
						onClick={(e) => console.log(e)}
						origin={[190, 34]}
						options={[
                            {yAccessor: ema26.accessor(), type: ema26.type(), stroke: ema26.stroke(), ...ema26.options(),},
						]}
				    />
					<MovingAverageTooltip
						onClick={(e) => console.log(e)}
						origin={[10, 34]}
						options={[
                            {yAccessor: ema20.accessor(), type: ema20.type(), stroke: ema20.stroke(), ...ema20.options(),},
						]}
				    />
