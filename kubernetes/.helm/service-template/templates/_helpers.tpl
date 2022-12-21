{{/*
Expand the name of the chart.
*/}}
{{- define "service-template.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "service-template.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "service-template.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "service-template.labels" -}}
helm.sh/chart: {{ include "service-template.chart" . }}
{{ include "service-template.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "service-template.selectorLabels" -}}
app.kubernetes.io/name: {{ include "service-template.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "service-template.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "service-template.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "service-template.image" -}}
{{- $tag := default .Chart.AppVersion .Values.image.tag -}}
{{- printf "%s:%s" .Values.image.name $tag -}}
{{- end -}}

{{- define "ingress-apis" }}
{{- if trimPrefix "v" .Capabilities.KubeVersion.Version | semverCompare ">1.19.0" }}
apiVersion: networking.k8s.io/v1
{{ else }}
apiVersion: extensions/v1beta1
{{- end }}
{{- end }}

{{- define "ingress-backend" }}
{{- $fullName := include "service-template.fullname" . -}}
{{- $svcPort := .Values.service.port -}}
{{- if trimPrefix "v" .Capabilities.KubeVersion.Version | semverCompare ">1.19.0" }}
          service:
            name: {{ $fullName }}
            port:
              number: {{ $svcPort }}
        pathType: Prefix
{{- else }}
          serviceName: {{ $fullName }}
          servicePort: {{ $svcPort }}
{{- end }}
{{- end }}
