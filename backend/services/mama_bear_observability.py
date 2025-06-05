"""
Professional Observability for Mama Bear (OpenTelemetry + Langfuse)
"""
import logging

try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False

try:
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False

logger = logging.getLogger("MamaBearObservability")

class ProfessionalObservability:
    def __init__(self, service_name="mama_bear_backend"):
        self.service_name = service_name
        self.tracer = None
        self.meter = None
        self.langfuse = None
        self.enabled = False
        self._init_otel()
        self._init_langfuse()

    def _init_otel(self):
        if not OPENTELEMETRY_AVAILABLE:
            logger.warning("OpenTelemetry not available, observability disabled.")
            return
        provider = TracerProvider()
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(self.service_name)
        self.enabled = True
        logger.info("OpenTelemetry tracing initialized.")
        # OTLP exporter config can be added here for production

    def _init_langfuse(self):
        if not LANGFUSE_AVAILABLE:
            logger.warning("Langfuse not available, LLM monitoring disabled.")
            return
        self.langfuse = Langfuse()
        logger.info("Langfuse LLM observability initialized.")

    def trace(self, name):
        if not self.enabled or not self.tracer:
            def dummy_decorator(func):
                return func
            return dummy_decorator
        def decorator(func):
            def wrapper(*args, **kwargs):
                with self.tracer.start_as_current_span(name):
                    return func(*args, **kwargs)
            return wrapper
        return decorator

    def log_llm_event(self, event_name, data):
        if self.langfuse:
            self.langfuse.log(event_name, data)
        else:
            logger.debug(f"LLM event: {event_name} | {data}")
